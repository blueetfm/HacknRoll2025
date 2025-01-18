'use client'

import React, { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Results from './components/Results'

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
    <main className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Digital Footprint Analyzer</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div>
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="Enter full name"
          />
        </div>
        <div>
          <Label htmlFor="school">School</Label>
          <Input
            id="school"
            type="text"
            value={school}
            onChange={(e) => setSchool(e.target.value)}
            required
            placeholder="Enter school name"
          />
        </div>
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Analyzing...' : 'Analyze Digital Footprint'}
        </Button>
      </form>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {results && <Results results={results} />}
    </main>
  )
}

