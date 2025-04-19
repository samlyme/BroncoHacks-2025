import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from claude_mcp_bridge import ClaudeMCPBridge, TopicRequest, StudyGuideRequest
import threading
from typing import Optional, Dict, Any, List
import json
import os

class MCPBridgeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Claude MCP Bridge")
        self.root.geometry("900x700")
        
        # Initialize bridge and start server
        self.bridge = ClaudeMCPBridge()
        self.bridge.start_server()
        
        # Store current topics and selected topic
        self.current_topics = []
        self.selected_topic = None
        
        self.setup_gui()
        self.setup_auto_refresh()
    
    def setup_gui(self):
        """Set up the GUI components"""
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TFrame", padding=5)
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Add buttons
        self.fetch_btn = ttk.Button(
            self.button_frame, 
            text="Fetch Questions",
            command=self.fetch_data
        )
        self.fetch_btn.pack(side=tk.LEFT, padx=5)
        
        # Add refresh button
        self.refresh_btn = ttk.Button(
            self.button_frame,
            text="🔄 Refresh",
            command=self.fetch_data
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Add auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=True)
        self.auto_refresh_check = ttk.Checkbutton(
            self.button_frame,
            text="Auto Refresh",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh
        )
        self.auto_refresh_check.pack(side=tk.LEFT, padx=5)
        
        # Create status label
        self.status_label = ttk.Label(self.button_frame, text="")
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Create connection status indicator
        self.connection_label = ttk.Label(
            self.button_frame, 
            text="●",
            foreground="gray"
        )
        self.connection_label.pack(side=tk.RIGHT, padx=5)
        
        # Create main display area with tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Questions tab
        self.questions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.questions_frame, text="User Questions")
        
        # Create questions display
        self.questions_text = scrolledtext.ScrolledText(
            self.questions_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 10)
        )
        self.questions_text.pack(fill=tk.BOTH, expand=True)
        
        # Statistics tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        
        # Create statistics display
        self.stats_text = scrolledtext.ScrolledText(
            self.stats_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 10)
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Topics tab
        self.topics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.topics_frame, text="Topics")
        
        # Create topics frame with split view
        self.setup_topics_frame()
        
        # Study Guide tab
        self.study_guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.study_guide_frame, text="Study Guide")
        
        # Create study guide interface
        self.setup_study_guide_frame()
        
        # Initialize search frame
        self.setup_search_frame()

    def setup_search_frame(self):
        """Set up the search functionality"""
        search_frame = ttk.Frame(self.questions_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def setup_topics_frame(self):
        """Set up the topics tab with topic list and detail view"""
        # Create paned window for split view
        paned_window = ttk.PanedWindow(self.topics_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Topic list
        left_frame = ttk.Frame(paned_window)
        
        # Add control frame for topic analysis
        topic_controls = ttk.Frame(left_frame)
        topic_controls.pack(fill=tk.X, padx=5, pady=5)
        
        # Add analyze button
        self.analyze_btn = ttk.Button(
            topic_controls,
            text="Analyze Topics",
            command=self.analyze_topics
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Add min questions entry
        ttk.Label(topic_controls, text="Min Questions:").pack(side=tk.LEFT, padx=5)
        self.min_questions_var = tk.StringVar(value="3")
        min_questions_entry = ttk.Entry(topic_controls, textvariable=self.min_questions_var, width=5)
        min_questions_entry.pack(side=tk.LEFT, padx=5)
        
        # Add topic listbox
        self.topic_listbox = tk.Listbox(
            left_frame,
            width=30,
            height=20,
            font=("Courier", 10),
            selectmode=tk.SINGLE
        )
        self.topic_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.topic_listbox.bind('<<ListboxSelect>>', self.on_topic_select)
        
        # Right side - Topic details
        right_frame = ttk.Frame(paned_window)
        
        # Add topic detail view
        self.topic_detail = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Courier", 10)
        )
        self.topic_detail.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add button to create study guide
        self.create_guide_btn = ttk.Button(
            right_frame,
            text="Create Study Guide",
            command=self.create_study_guide_from_topic,
            state=tk.DISABLED
        )
        self.create_guide_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Add frames to paned window
        paned_window.add(left_frame, weight=1)
        paned_window.add(right_frame, weight=2)

    def setup_study_guide_frame(self):
        """Set up the study guide tab"""
        # Top controls
        controls_frame = ttk.Frame(self.study_guide_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Topic selection
        ttk.Label(controls_frame, text="Topic:").pack(side=tk.LEFT, padx=5)
        self.topic_var = tk.StringVar()
        self.topic_combo = ttk.Combobox(controls_frame, textvariable=self.topic_var, width=30)
        self.topic_combo.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        self.generate_btn = ttk.Button(
            controls_frame,
            text="Generate Guide",
            command=self.generate_study_guide
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_btn = ttk.Button(
            controls_frame,
            text="Save Guide",
            command=self.save_study_guide,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.RIGHT, padx=5)
        
        # Study guide display
        self.guide_text = scrolledtext.ScrolledText(
            self.study_guide_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Courier", 10)
        )
        self.guide_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_auto_refresh(self):
        """Set up auto-refresh functionality"""
        self.auto_refresh_active = True
        self.schedule_refresh()

    def schedule_refresh(self):
        """Schedule the next auto-refresh"""
        if self.auto_refresh_active and self.auto_refresh_var.get():
            self.root.after(5000, self.auto_refresh)

    def auto_refresh(self):
        """Perform auto-refresh"""
        self.fetch_data()
        self.schedule_refresh()

    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        if self.auto_refresh_var.get():
            self.schedule_refresh()

    def show_status(self, message: str, is_error: bool = False):
        """Update status label with message"""
        self.status_label.config(
            text=message,
            foreground="red" if is_error else "green"
        )
        self.root.after(3000, lambda: self.status_label.config(text=""))

    def update_connection_status(self, is_connected: bool):
        """Update the connection status indicator"""
        self.connection_label.config(
            foreground="green" if is_connected else "red",
            text="●"
        )

    def fetch_data(self):
        """Fetch and display data"""
        try:
            # Check connection
            is_connected = self.bridge.health_check()
            self.update_connection_status(is_connected)
            
            if not is_connected:
                raise ConnectionError("MCP server is not responding")
            
            # Fetch questions
            questions = self.bridge.fetch_user_questions()
            
            # Store questions for searching
            self.current_questions = questions
            
            # Display questions
            self.display_questions(questions)
            
            # Calculate and display statistics
            stats = self.bridge.calculate_statistics(questions)
            self.display_statistics(stats)
            
            self.show_status(f"Successfully fetched {len(questions)} questions")
            
        except Exception as e:
            self.show_status(f"Error: {str(e)}", is_error=True)

    def display_questions(self, questions):
        """Display questions in the text widget"""
        self.questions_text.delete(1.0, tk.END)
        self.questions_text.insert(tk.END, "User Questions:\n\n")
        
        for i, q in enumerate(questions, 1):
            self.questions_text.insert(
                tk.END, 
                f"{i}. {q['content']}\n\n"
            )

    def display_statistics(self, stats):
        """Display statistics in the stats tab"""
        self.stats_text.delete(1.0, tk.END)
        
        stats_text = f"""Question Statistics:
        
Total Questions: {stats['total_questions']}
Average Length: {stats['average_length']:.1f} characters

Question Length Distribution:
"""
        
        for category, count in stats['length_distribution'].items():
            percentage = (count / stats['total_questions'] * 100) if stats['total_questions'] > 0 else 0
            stats_text += f"{category}: {count} ({percentage:.1f}%)\n"
        
        self.stats_text.insert(tk.END, stats_text)

    def on_search_change(self, *args):
        """Handle search input changes"""
        search_term = self.search_var.get().lower()
        
        if hasattr(self, 'current_questions'):
            filtered_questions = [
                q for q in self.current_questions 
                if search_term in q['content'].lower()
            ]
            self.display_questions(filtered_questions)
    
    def analyze_topics(self):
        """Analyze question topics using Claude"""
        try:
            # Check connection
            if not self.bridge.health_check():
                raise ConnectionError("MCP server is not responding")
            
            # Show processing status
            self.show_status("Analyzing topics, please wait...")
            
            # Disable analyze button while processing
            self.analyze_btn.config(state=tk.DISABLED)
            
            # Get min questions value
            try:
                min_questions = int(self.min_questions_var.get())
            except ValueError:
                min_questions = 3
            
            # Run in a separate thread to keep UI responsive
            def run_analysis():
                try:
                    # Make API call to analyze topics
                    request = TopicRequest(
                        limit=500,
                        min_questions=min_questions
                    )
                    topics_data = self.bridge.identify_question_topics(
                        [q['content'] for q in self.current_questions],
                        min_questions
                    )
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.display_topics(topics_data))
                    self.root.after(0, lambda: self.show_status("Topic analysis complete"))
                except Exception as e:
                    self.root.after(0, lambda: self.show_status(f"Error: {str(e)}", is_error=True))
                finally:
                    # Re-enable the button
                    self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
            
            # Start analysis thread
            threading.Thread(target=run_analysis, daemon=True).start()
            
        except Exception as e:
            self.show_status(f"Error: {str(e)}", is_error=True)
            self.analyze_btn.config(state=tk.NORMAL)
    
    def display_topics(self, topics_data):
        """Display topics in the topics tab"""
        # Clear current topics
        self.topic_listbox.delete(0, tk.END)
        self.topic_detail.delete(1.0, tk.END)
        
        # Get topics list
        if 'common_topics' in topics_data:
            topics = topics_data['common_topics']
            self.current_topics = topics
            
            # Update topic combobox for study guide tab
            topic_titles = [topic['title'] for topic in topics]
            self.topic_combo['values'] = topic_titles
            
            # Update topics listbox
            for topic in topics:
                self.topic_listbox.insert(tk.END, topic['title'])
        else:
            self.show_status("No topics found", is_error=True)
    
    def on_topic_select(self, event):
        """Handle topic selection from listbox"""
        selection = self.topic_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.current_topics):
            # Get selected topic
            topic = self.current_topics[index]
            self.selected_topic = topic
            
            # Display topic details
            self.topic_detail.delete(1.0, tk.END)
            
            # Format topic details
            detail_text = f"Topic: {topic['title']}\n\n"
            detail_text += "Example Questions:\n"
            for i, example in enumerate(topic['examples'], 1):
                detail_text += f"{i}. {example}\n\n"
            
            detail_text += f"Explanation:\n{topic['explanation']}\n"
            
            self.topic_detail.insert(tk.END, detail_text)
            
            # Enable study guide button
            self.create_guide_btn.config(state=tk.NORMAL)
    
    def create_study_guide_from_topic(self):
        """Create study guide from selected topic"""
        if not self.selected_topic:
            return
        
        # Switch to study guide tab
        self.notebook.select(self.study_guide_frame)
        
        # Set topic in combobox
        self.topic_var.set(self.selected_topic['title'])
        
        # Generate study guide
        self.generate_study_guide()
    
    def generate_study_guide(self):
        """Generate study guide for selected topic"""
        topic_title = self.topic_var.get()
        if not topic_title:
            self.show_status("Please select a topic", is_error=True)
            return
        
        # Find topic data
        topic_data = None
        for topic in self.current_topics:
            if topic['title'] == topic_title:
                topic_data = topic
                break
        
        if not topic_data:
            self.show_status("Topic not found", is_error=True)
            return
        
        # Show processing status
        self.show_status("Generating study guide, please wait...")
        
        # Disable generate button while processing
        self.generate_btn.config(state=tk.DISABLED)
        
        # Run in a separate thread to keep UI responsive
        def run_generation():
            try:
                # Generate study guide
                study_guide = self.bridge.generate_study_guide(
                    topic=topic_data['title'],
                    examples=topic_data['examples']
                )
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_study_guide(study_guide))
                self.root.after(0, lambda: self.show_status("Study guide generated"))
                self.root.after(0, lambda: self.save_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.root.after(0, lambda: self.show_status(f"Error: {str(e)}", is_error=True))
            finally:
                # Re-enable the button
                self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
        
        # Start generation thread
        threading.Thread(target=run_generation, daemon=True).start()
    
    def display_study_guide(self, study_guide):
        """Display generated study guide"""
        self.guide_text.delete(1.0, tk.END)
        self.guide_text.insert(tk.END, study_guide)
    
    def save_study_guide(self):
        """Save study guide to file"""
        if not self.guide_text.get(1.0, tk.END).strip():
            self.show_status("No study guide to save", is_error=True)
            return
        
        # Get topic title for default filename
        topic_title = self.topic_var.get()
        if topic_title:
            default_filename = topic_title.lower().replace(" ", "_").replace("/", "_") + ".md"
        else:
            default_filename = "study_guide.md"
        
        # Open file dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filepath:
            return
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.guide_text.get(1.0, tk.END))
            
            self.show_status(f"Study guide saved to {filepath}")
        except Exception as e:
            self.show_status(f"Error saving file: {str(e)}", is_error=True)

def main():
    root = tk.Tk()
    app = MCPBridgeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()