'use client'

import React, { useState } from 'react'
import { 
  Button, 
  TextField, 
  Container, 
  Typography, 
  Box,
  CircularProgress
} from '@mui/material'
import Results from './components/Results'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'

const theme = createTheme({
  palette: {
    mode: 'light',
  },
})

export default function Home() {
  const [name, setName] = useState('')
  const [school, setSchool] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, school }),
      })
      if (!response.ok) {
        throw new Error('Failed to analyze data')
      }
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
      setError('An error occurred while analyzing the data. Please try again.')
    }
    setLoading(false)
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="sm">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Digital Footprint Analyzer
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="name"
              label="Name"
              name="name"
              autoComplete="name"
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="school"
              label="School"
              name="school"
              autoComplete="school"
              value={school}
              onChange={(e) => setSchool(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Analyze Digital Footprint'}
            </Button>
          </Box>
          {error && (
            <Typography color="error" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
          {results && <Results results={results} />}
        </Box>
      </Container>
    </ThemeProvider>
  )
}
