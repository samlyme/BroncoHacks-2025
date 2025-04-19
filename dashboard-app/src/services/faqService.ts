import { FAQ } from '../components/FaqList';

// Mock data - this will be replaced with API call later
const dummyFaqs: FAQ[] = [
  {
    id: 1,
    question: "What is the registration deadline?",
    answer: "The registration deadline is October 15th, 2025. Make sure to complete all required forms before this date.",
    frequency: 156
  },
  {
    id: 2,
    question: "How many team members can participate?",
    answer: "Teams can have between 2-4 members. Solo participants are also welcome but encouraged to join teams.",
    frequency: 142
  },
  {
    id: 3,
    question: "Are there any prerequisites for participation?",
    answer: "No specific prerequisites are required. Participants of all skill levels are welcome to join.",
    frequency: 89
  },
  {
    id: 4,
    question: "Will there be food provided?",
    answer: "Yes, meals and snacks will be provided throughout the event. Please let us know about any dietary restrictions.",
    frequency: 201
  },
  {
    id: 5,
    question: "What should I bring to the hackathon?",
    answer: "Please bring your laptop, charger, and any other devices you might need. Consider bringing a water bottle and comfortable clothes.",
    frequency: 178
  },
  {
    id: 6,
    question: "Is there a dress code?",
    answer: "Casual attire is recommended. Wear comfortable clothes as you'll be sitting for extended periods.",
    frequency: 58
  },
  {
    id: 7,
    question: "What are the prizes?",
    answer: "Prizes include cash rewards, tech gadgets, and opportunities for internships with our sponsors.",
    frequency: 225
  },
  {
    id: 8,
    question: "Will there be mentors available?",
    answer: "Yes, industry professionals will be available throughout the event to provide guidance and support.",
    frequency: 104
  }
];

// Simulates an API call with delay
export const fetchFaqs = async (): Promise<FAQ[]> => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Return mock data - sort by frequency by default
  return [...dummyFaqs].sort((a, b) => b.frequency - a.frequency);
};

// For future implementation
export const searchFaqs = async (query: string): Promise<FAQ[]> => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 300));
  
  // Filter FAQs based on query
  return dummyFaqs.filter(
    faq => 
      faq.question.toLowerCase().includes(query.toLowerCase()) || 
      faq.answer.toLowerCase().includes(query.toLowerCase())
  );
}; 