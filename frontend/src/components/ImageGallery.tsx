'use client'

import { useEffect, useState } from 'react'
import { supabase } from '../utils/supabase-client'
import Image from 'next/image'
import { useAuth } from '../contexts/AuthContext'

interface ImageRecord {
  id: number
  file_name: string
  created_at: string
  user_id: string
  url: string
}

export default function ImageGallery() {
  const [images, setImages] = useState<ImageRecord[]>([])
  const { user } = useAuth()

  useEffect(() => {
    if (user) {
      fetchImages()
    }
  }, [user])

  async function fetchImages() {
    if (!user) return

    const { data, error } = await supabase
      .from('images')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching images:', error)
    } else {
      setImages(data || [])
    }
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {images.map((image) => (
        <div key={image.id} className="relative aspect-square">
          <Image
            src={image.url || "/placeholder.svg"}
            alt={`Uploaded image ${image.id}`}
            fill
            className="object-cover rounded-lg"
          />
          <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white p-2 text-sm">
            <p>File: {image.file_name}</p>
            <p>Uploaded: {new Date(image.created_at).toLocaleString()}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

