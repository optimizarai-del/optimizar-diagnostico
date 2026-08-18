import { Navigate, Route, Routes } from 'react-router-dom'

import RedNodos from './components/RedNodos'
import Diagnostico from './pages/Diagnostico'
import Formulario from './pages/Formulario'
import Landing from './pages/Landing'

export default function App() {
  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <RedNodos />
      <div className="relative z-10">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/diagnostico" element={<Formulario />} />
          <Route path="/d/:token" element={<Diagnostico />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  )
}
