import { Author, SocialNetwork } from './types';
import { Linkedin, Instagram, Facebook, Send } from 'lucide-react';

export const AUTHORS: Author[] = [
  {
    id: 'person_01',
    name: 'Alex Rivera',
    role: 'Tech Lead',
    avatar: 'https://picsum.photos/id/64/200/200',
    stats: { formality: 'High', avgLength: 1200, emojiDensity: 'Low' },
    samplePosts: [
      "In my experience, scaling microservices requires a fundamental shift in team culture, not just technology. #TechLeadership #DevOps",
      "Just finished a deep dive into Rust memory safety guarantees. The learning curve is steep, but the payoff for system stability is undeniable.",
      "Efficiency isn't about working harder; it's about eliminating the friction in your deployment pipeline."
    ]
  },
  {
    id: 'person_02',
    name: 'Sarah Chen',
    role: 'Product Manager',
    avatar: 'https://picsum.photos/id/65/200/200',
    stats: { formality: 'Medium', avgLength: 850, emojiDensity: 'Medium' },
    samplePosts: [
      "User empathy is the most underrated skill in product management. ❤️ Talk to your users every single day!",
      "Launching a feature is just the beginning. The real work starts when the feedback loops open. 🚀 #ProductLife",
      "Big shoutout to the design team for nailing the new onboarding flow. Conversion rates are up 15% this week! 📈"
    ]
  },
  {
    id: 'person_03',
    name: 'Dmitry Volkov',
    role: 'Startup Founder',
    avatar: 'https://picsum.photos/id/91/200/200',
    stats: { formality: 'Low', avgLength: 400, emojiDensity: 'High' },
    samplePosts: [
      "Sleep is for the weak? No. Sleep is for those who want to win the marathon, not just the sprint. 😴💪",
      "Just closed our seed round! incredible feeling. Now the real grind begins. 🔥🚀",
      "Don't listen to the haters. Build what you love. Break things. Fix them. Repeat."
    ]
  }
];

export const SOCIAL_NETWORKS: { id: SocialNetwork; name: string; icon: any; color: string }[] = [
  { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700' },
  { id: 'instagram', name: 'Instagram', icon: Instagram, color: 'text-pink-600' },
  { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600' },
  { id: 'telegram', name: 'Telegram', icon: Send, color: 'text-sky-500' },
];

export const MOCK_TOPICS = [
  "The future of remote work in 2025",
  "Why I switched from React to Vue (and back)",
  "3 lessons learned from my failed startup",
  "The ethics of AI in creative industries",
  "How to manage burnout as a developer",
  "My morning routine for maximum productivity",
  "The importance of soft skills in tech",
  "Web3: Revolution or passing fad?",
  "Leading a team through uncertainty",
  "The best coding advice I ever received"
];

export const MOCK_DELAY_MS = 2000;