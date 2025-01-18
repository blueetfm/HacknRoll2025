import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Chip,
  LinearProgress
} from '@mui/material'

interface ResultsProps {
  results: {
    overallSentiment: string
    sentimentScore: number
    topKeywords: string[]
  }
}

export default function Results({ results }: ResultsProps) {
  const { overallSentiment, sentimentScore, topKeywords } = results

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'success.main'
      case 'negative':
        return 'error.main'
      default:
        return 'warning.main'
    }
  }

  return (
    <Card sx={{ mt: 4 }}>
      <CardContent>
        <Typography variant="h5" component="div" gutterBottom>
          Analysis Results
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1" component="span">
            Overall Sentiment:{' '}
          </Typography>
          <Typography 
            variant="body1" 
            component="span" 
            color={getSentimentColor(overallSentiment)}
            fontWeight="bold"
          >
            {overallSentiment}
          </Typography>
        </Box>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1" gutterBottom>
            Sentiment Score: {sentimentScore.toFixed(2)}
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={(sentimentScore + 1) * 50} 
            sx={{ height: 10, borderRadius: 5 }}
          />
        </Box>
        <Box>
          <Typography variant="body1" gutterBottom>
            Top Keywords:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {topKeywords.map((keyword, index) => (
              <Chip key={index} label={keyword} variant="outlined" />
            ))}
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}

