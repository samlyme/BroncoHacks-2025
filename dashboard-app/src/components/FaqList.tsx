'use client';

import { 
  Typography, 
  Box, 
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  LinearProgress,
  Chip,
  Card,
  CardContent,
  useTheme,
  alpha
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import PeopleIcon from '@mui/icons-material/People';
import StarIcon from '@mui/icons-material/Star';

// Define FAQ type
export interface FAQ {
  id: number;
  question: string;
  answer: string;
  frequency: number;
}

interface FaqListProps {
  faqs: FAQ[];
  isLoading?: boolean;
  error?: string;
}

export default function FaqList({ faqs, isLoading = false, error }: FaqListProps) {
  const theme = useTheme();

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" py={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box py={2}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!faqs || faqs.length === 0) {
    return (
      <Box py={2}>
        <Typography>No FAQs available at this time.</Typography>
      </Box>
    );
  }

  // Calculate total frequency for percentage calculations
  const totalFrequency = faqs.reduce((sum, faq) => sum + faq.frequency, 0);
  
  // Get top 3 FAQs for summary cards
  const topThreeFaqs = faqs.slice(0, 3);

  return (
    <>
      {/* Dashboard Summary Cards */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: 3, mb: 4 }}>
        <Box sx={{ gridColumn: { xs: 'span 12', md: 'span 4' } }}>
          <Card 
            sx={{ 
              height: '100%',
              background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.2)} 100%)`,
              border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`
            }}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <QuestionAnswerIcon sx={{ color: theme.palette.primary.main, mr: 1 }} />
                <Typography color="text.secondary" variant="subtitle2">
                  Total Questions
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ color: theme.palette.primary.main }}>
                {faqs.length}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ gridColumn: { xs: 'span 12', md: 'span 4' } }}>
          <Card 
            sx={{ 
              height: '100%',
              background: `linear-gradient(135deg, ${alpha(theme.palette.success.main, 0.1)} 0%, ${alpha(theme.palette.success.main, 0.2)} 100%)`,
              border: `1px solid ${alpha(theme.palette.success.main, 0.1)}`
            }}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PeopleIcon sx={{ color: theme.palette.success.main, mr: 1 }} />
                <Typography color="text.secondary" variant="subtitle2">
                  Total Inquiries
                </Typography>
              </Box>
              <Typography variant="h4" sx={{ color: theme.palette.success.main }}>
                {totalFrequency}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ gridColumn: { xs: 'span 12', md: 'span 4' } }}>
          <Card 
            sx={{ 
              height: '100%',
              background: `linear-gradient(135deg, ${alpha(theme.palette.warning.main, 0.1)} 0%, ${alpha(theme.palette.warning.main, 0.2)} 100%)`,
              border: `1px solid ${alpha(theme.palette.warning.main, 0.1)}`
            }}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <StarIcon sx={{ color: theme.palette.warning.main, mr: 1 }} />
                <Typography color="text.secondary" variant="subtitle2">
                  Most Asked Question
                </Typography>
              </Box>
              <Typography variant="body1" noWrap sx={{ fontWeight: 'medium' }}>
                {faqs[0]?.question}
              </Typography>
              <Typography variant="h5" sx={{ color: theme.palette.warning.main, mt: 1 }}>
                {faqs[0]?.frequency}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Top 3 Most Asked Questions with Progress Bars */}
      <Paper 
        elevation={0} 
        sx={{ 
          p: 3, 
          mb: 4, 
          borderRadius: 2,
          border: `1px solid ${theme.palette.divider}`
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <TrendingUpIcon sx={{ mr: 1, color: theme.palette.primary.main }} />
          <Typography variant="h6">
            Top Questions
          </Typography>
        </Box>
        
        {topThreeFaqs.map((faq, index) => (
          <Box key={faq.id} sx={{ mb: index < topThreeFaqs.length - 1 ? 3 : 0 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
              <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                {faq.question}
              </Typography>
              <Chip 
                label={`${faq.frequency} (${Math.round((faq.frequency / totalFrequency) * 100)}%)`} 
                size="small" 
                color="primary"
                variant="outlined"
              />
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={(faq.frequency / totalFrequency) * 100} 
              sx={{ 
                height: 8, 
                borderRadius: 5,
                backgroundColor: alpha(theme.palette.primary.main, 0.1),
                '& .MuiLinearProgress-bar': {
                  borderRadius: 5,
                  backgroundImage: `linear-gradient(90deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`
                }
              }}
            />
          </Box>
        ))}
      </Paper>

      {/* Full Data Table */}
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>Rank</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>Question</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>Answer</TableCell>
              <TableCell align="right" sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>Frequency</TableCell>
              <TableCell align="right" sx={{ fontWeight: 'bold', color: theme.palette.text.primary }}>Percentage</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {faqs.map((faq, index) => (
              <TableRow 
                key={faq.id}
                sx={{ 
                  '&:nth-of-type(odd)': { 
                    backgroundColor: alpha(theme.palette.primary.main, 0.02)
                  },
                  '&:hover': {
                    backgroundColor: alpha(theme.palette.primary.main, 0.05)
                  }
                }}
              >
                <TableCell component="th" scope="row">
                  {index + 1}
                </TableCell>
                <TableCell>{faq.question}</TableCell>
                <TableCell>{faq.answer}</TableCell>
                <TableCell align="right">
                  <Typography fontWeight="medium" color="primary">
                    {faq.frequency}
                  </Typography>
                </TableCell>
                <TableCell align="right">
                  <Chip 
                    label={`${Math.round((faq.frequency / totalFrequency) * 100)}%`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
} 