'use client'

import { useState } from 'react'
import { supabase } from '../utils/supabase-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAuth } from '../contexts/AuthContext'

export default function ImageUploadForm() {
  const { user } = useAuth()
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!file) return
    if (!user) {
      alert('Please sign in to upload images')
      return
    }

    setUploading(true)
    try {
      const fileExt = file.name.split('.').pop()
      const fileName = `${Math.random()}.${fileExt}`
      const filePath = `${user.id}/${fileName}`

      const { data, error } = await supabase.storage
        .from('images')
        .upload(filePath, file)

      if (error) throw error

      const { data: publicUrlData } = supabase.storage
        .from('images')
        .getPublicUrl(filePath)

      const { data: insertData, error: insertError } = await supabase
        .from('images')
        .insert({
          file_name: fileName,
          user_id: user.id,
          url: publicUrlData.publicUrl
        })

      if (insertError) throw insertError

      alert('Image uploaded successfully!')
    } catch (error) {
      console.error('Error uploading image:', error)
      alert('Error uploading image')
    } finally {
      setUploading(false)
      setFile(null)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input type="file" onChange={handleFileChange} accept="image/*" />
      <Button type="submit" disabled={!file || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </Button>
    </form>
  )
}

