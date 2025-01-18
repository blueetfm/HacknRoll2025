import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const body = await req.json()
  const { name, school } = body

  try {
    // Make an API call to your Python backend
    const response = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, school }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json({ error: 'Failed to analyze data' }, { status: 500 })
  }
}

