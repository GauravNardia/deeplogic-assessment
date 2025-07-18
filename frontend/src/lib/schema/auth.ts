import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email({ message: 'Invalid email' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' })
});


export const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
  role: z.enum(['REPORTER', 'MAINTAINER', 'ADMIN']),
});
