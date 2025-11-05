# Research Paper Q&A Frontend

An elegant and minimalistic React frontend for the Research Paper Q&A application.

## Features

- 🎨 **Modern UI**: Clean, minimalistic design with Tailwind CSS
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices
- 📄 **PDF Upload**: Drag & drop or click to upload research papers
- 💬 **Real-time Chat**: Interactive chat interface with conversation history
- 📚 **Source Documents**: Sidebar showing relevant document chunks used for answers
- 🔄 **Session Management**: Start new conversations or clear all data
- ⚡ **Fast**: Built with Vite for optimal performance

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and visit `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. If your backend runs on a different port, update the `vite.config.js` file:

```javascript
export default defineConfig({
  // ...
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:YOUR_BACKEND_PORT', // Change this
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

## Usage

1. **Upload PDF**: Drag and drop a research paper PDF or click to browse
2. **Ask Questions**: Type your questions in the chat input
3. **View Sources**: Check the sidebar to see which document chunks were used
4. **Manage Sessions**: Use "New Chat" to start fresh or "Clear All" to remove everything

## API Integration

The frontend communicates with the FastAPI backend through these endpoints:

- `POST /upload-pdf` - Upload and process PDF files
- `POST /chat` - Send questions and receive answers
- `POST /new-session` - Start a new conversation thread
- `DELETE /clear-all` - Clear all data

## Customization

### Colors
Update the color scheme in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
      }
    }
  }
}
```

### Styling
Modify component styles in `src/index.css` or directly in components using Tailwind classes.

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory, ready for deployment.

## Deployment

You can deploy the built frontend to any static hosting service like:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Make sure to update the API base URL for production deployment.
