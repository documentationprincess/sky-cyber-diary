import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    caseNumber: z.string(),
    status: z.enum(['open', 'solved', 'ongoing']).default('ongoing'),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    readTime: z.string().optional(),
    aiGrade: z.string().optional()
  })
});

export const collections = { posts };
