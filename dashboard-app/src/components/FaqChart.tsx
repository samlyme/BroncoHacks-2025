'use client';

import { 
  Box,
  Paper,
  Typography,
  useTheme,
  alpha
} from '@mui/material';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import AssessmentIcon from '@mui/icons-material/Assessment';

interface FAQ {
  id: number;
  question: string;
  answer: string;
  frequency: number;
}

interface FaqChartProps {
  faqs: FAQ[];
}

// Professional color palette
const COLORS = [
  '#2196F3', // Primary Blue
  '#00C853', // Success Green
  '#FFB300', // Warning Amber
  '#E91E63', // Pink
  '#673AB7', // Deep Purple
];

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text 
      x={x} 
      y={y} 
      fill="white" 
      textAnchor={x > cx ? 'start' : 'end'} 
      dominantBaseline="central"
      style={{ fontSize: '14px', fontWeight: 500 }}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

export default function FaqChart({ faqs }: FaqChartProps) {
  const theme = useTheme();
  
  // Prepare data for the chart - take top 5 FAQs
  const chartData = faqs.slice(0, 5).map(faq => ({
    name: faq.question.length > 30 ? faq.question.substring(0, 30) + '...' : faq.question,
    value: faq.frequency,
    fullQuestion: faq.question,
    color: COLORS[0]
  }));

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        p: 3, 
        mb: 4, 
        borderRadius: 2,
        border: `1px solid ${theme.palette.divider}`,
        background: theme.palette.background.paper
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <AssessmentIcon sx={{ mr: 1, color: theme.palette.primary.main }} />
        <Typography variant="h6">
          Question Distribution Analysis
        </Typography>
      </Box>
      <Box sx={{ width: '100%', height: 400, mt: 2 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomizedLabel}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]}
                  stroke={theme.palette.background.paper}
                  strokeWidth={2}
                />
              ))}
            </Pie>
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length > 0 && payload[0]?.payload) {
                  const data = payload[0].payload;
                  const colorIndex = data.index !== undefined ? data.index % COLORS.length : 0;
                  return (
                    <Paper 
                      elevation={3}
                      sx={{ 
                        p: 2, 
                        backgroundColor: theme.palette.background.paper,
                        border: `1px solid ${alpha(COLORS[colorIndex], 0.2)}`,
                        boxShadow: `0 4px 20px 0 ${alpha(theme.palette.common.black, 0.1)}`
                      }}
                    >
                      <Typography variant="subtitle2" sx={{ mb: 1, color: theme.palette.text.secondary }}>
                        {data.fullQuestion}
                      </Typography>
                      <Typography variant="body1" sx={{ color: COLORS[colorIndex], fontWeight: 600 }}>
                        Frequency: {data.value}
                      </Typography>
                    </Paper>
                  );
                }
                return null;
              }}
            />
            <Legend 
              verticalAlign="bottom" 
              height={48}
              formatter={(value, entry: any) => (
                <Typography 
                  variant="body2" 
                  sx={{ 
                    maxWidth: 200,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                    color: theme.palette.text.primary
                  }}
                >
                  {value}
                </Typography>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
} 