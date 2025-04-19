'use client';

import { useState, useEffect } from 'react';
import { 
  Typography, 
  Container, 
  Box,
  CircularProgress,
  Paper,
  Divider,
  useTheme
} from '@mui/material';
import FaqList, { FAQ } from '@/components/FaqList';
import FaqChart from '@/components/FaqChart';
import { fetchFaqs } from '@/services/faqService';
import BarChartIcon from '@mui/icons-material/BarChart';

export default function Home() {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  // Load initial data
  useEffect(() => {
    const loadFaqs = async () => {
      try {
        setIsLoading(true);
        const data = await fetchFaqs();
        setFaqs(data);
        setError(null);
      } catch (err) {
        setError('Failed to load FAQs. Please try again later.');
        console.error('Error loading FAQs:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadFaqs();
  }, []);

  if (isLoading) {
    return (
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Typography color="error">{error}</Typography>
      </Container>
    );
  }

  return (
    <Box 
      sx={{ 
        minHeight: '100vh',
        backgroundColor: theme.palette.grey[100],
        pt: 4,
        pb: 8
      }}
    >
      <Container maxWidth="lg">
        {/* Header Section */}
        <Paper 
          elevation={0} 
          sx={{ 
            p: 4, 
            mb: 4, 
            borderRadius: 2,
            background: 'linear-gradient(120deg, #2196F3 0%, #1976D2 100%)',
            color: 'white'
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <BarChartIcon sx={{ fontSize: 40, mr: 2 }} />
            <Typography variant="h3" component="h1" fontWeight="500">
              FAQ Analytics Dashboard
            </Typography>
          </Box>
          <Typography variant="h6" sx={{ opacity: 0.9, fontWeight: 'normal' }}>
            Real-time analysis of frequently asked questions and their distribution
          </Typography>
        </Paper>

        {/* Main Content */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {/* Chart Section */}
          <FaqChart faqs={faqs} />
          
          {/* Data Table Section */}
          <Paper elevation={0} sx={{ p: 3, borderRadius: 2 }}>
            <Typography 
              variant="h5" 
              gutterBottom 
              sx={{ 
                mb: 3, 
                fontWeight: 500,
                color: theme.palette.text.primary 
              }}
            >
              Detailed FAQ Analysis
            </Typography>
            <Divider sx={{ mb: 3 }} />
            <FaqList 
              faqs={faqs} 
              isLoading={isLoading} 
              error={error || undefined}
            />
          </Paper>
        </Box>
      </Container>
    </Box>
  );
}
