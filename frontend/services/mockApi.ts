import { GenerateRequest, GenerateResponse, SocialNetwork } from '../types';
import { MOCK_DELAY_MS } from '../constants';

// Helper to generate text based on inputs
const generateMockText = (topic: string, network: SocialNetwork, authorId: string): string => {
  const base = `Here are my thoughts on "${topic}".`;
  
  if (network === 'linkedin') {
    return `${base} \n\nLooking back at my journey, I realize that professional growth is rarely linear. It takes resilience and strategic thinking.\n\nKey takeaways:\n1. Always value your team.\n2. Embrace change.\n3. Focus on long-term impact.\n\nWhat are your thoughts? 👇\n\n#Leadership #ProfessionalGrowth #CareerDevelopment`;
  }
  
  if (network === 'instagram') {
    return `${base} ✨\n\nSometimes you just have to trust the process. 🌿\n\nSwipe left to see how we made it happen! 👉\n.\n.\n.\n#Motivation #DailyGrind #Inspiration #TechLife`;
  }
  
  if (network === 'telegram') {
    return `⚡️ **Quick update on: ${topic}**\n\nHonestly, I think most people get this wrong. The industry is shifting fast.\n\nCheck out the link below for the full breakdown.\n\n(Link in bio)`;
  }
  
  return `${base} It's been an interesting week reflecting on this. I'd love to hear what my friends think about it.`;
};

export const generatePost = async (request: GenerateRequest): Promise<GenerateResponse> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        generated_post: generateMockText(request.topic, request.social_network, request.author_id),
        style_similarity: parseFloat((0.75 + Math.random() * 0.2).toFixed(2)), // Random between 0.75 and 0.95
        debug: {
          target_length: request.social_network === 'linkedin' ? 1200 : 300,
          model_version: 'diffuzio-v1.4-fine-tuned',
          processing_time_ms: 1450,
          prompt_tokens: 342
        }
      });
    }, MOCK_DELAY_MS);
  });
};