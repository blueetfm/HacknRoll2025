import ImageUploadForm from '../components/ImageUploadForm'
import ImageGallery from '../components/ImageGallery'
import { AuthProvider } from '../contexts/AuthContext'
import Auth from '../components/Auth'

export default function Home() {
  return (
    <AuthProvider>
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-8">Image Upload App</h1>
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Authentication</h2>
          <Auth />
        </div>
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Upload an Image</h2>
          <ImageUploadForm />
        </div>
        <div>
          <h2 className="text-2xl font-semibold mb-4">Uploaded Images</h2>
          <ImageGallery />
        </div>
      </div>
    </AuthProvider>
  )
}