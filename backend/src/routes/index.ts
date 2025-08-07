import express from 'express';
import authRoutes from './auth.routes';

const router = express.Router();

// API routes
router.use('/auth', authRoutes);

// Health check
router.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date() });
});

export default router;