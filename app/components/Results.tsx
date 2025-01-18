import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

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
        return 'text-green-600'
      case 'negative':
        return 'text-red-600'
      default:
        return 'text-yellow-600'
    }
  }

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle>Analysis Results</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <strong>Overall Sentiment:</strong>{' '}
          <span className={getSentimentColor(overallSentiment)}>{overallSentiment}</span>
        </div>
        <div>
          <strong>Sentiment Score:</strong> {sentimentScore.toFixed(2)}
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: `${(sentimentScore + 1) * 50}%` }}
            ></div>
          </div>
        </div>
        <div>
          <strong>Top Keywords:</strong>
          <div className="flex flex-wrap gap-2 mt-2">
            {topKeywords.map((keyword, index) => (
              <span key={index} className="px-2 py-1 bg-gray-200 rounded-full text-sm">
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

