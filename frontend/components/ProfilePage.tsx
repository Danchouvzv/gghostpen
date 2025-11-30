import React, { useState, useEffect } from 'react';
import { User, Plus, Trash2, RefreshCw, FileText, Linkedin, Instagram, Facebook, MessageCircle, Loader2, Check, X } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

interface Post {
  id: string;
  platform: string;
  content: string;
  timestamp: string;
  hashtags: string[];
  mentions: string[];
  emojis: string[];
}

interface ProfilePageProps {
  userId: string;
  userName: string;
  onBack: () => void;
}

const ProfilePage: React.FC<ProfilePageProps> = ({ userId, userName, onBack }) => {
  const { t } = useLanguage();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [rebuilding, setRebuilding] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  
  // Form state
  const [platform, setPlatform] = useState<'linkedin' | 'instagram' | 'facebook' | 'telegram'>('linkedin');
  const [content, setContent] = useState('');
  const [hashtags, setHashtags] = useState('');
  const [emojis, setEmojis] = useState('');

  const loadPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/users/${userId}/posts`);
      if (response.ok) {
        const data = await response.json();
        setPosts(data.posts || []);
      }
    } catch (error) {
      console.error('Ошибка загрузки постов:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPosts();
  }, [userId]);

  const handleAddPost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    setSubmitting(true);
    try {
      const hashtagsArray = hashtags.split(',').map(h => h.trim()).filter(h => h && h.startsWith('#'));
      const emojisArray = emojis.split('').filter(e => /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]/u.test(e));

      const response = await fetch(`http://localhost:8000/api/users/${userId}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platform,
          content: content.trim(),
          hashtags: hashtagsArray,
          emojis: emojisArray,
        }),
      });

      if (response.ok) {
        setContent('');
        setHashtags('');
        setEmojis('');
        setShowAddForm(false);
        await loadPosts();
      } else {
        const error = await response.json();
        alert(error.detail || 'Ошибка добавления поста');
      }
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Ошибка добавления поста');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeletePost = async (postId: string) => {
    if (!confirm(t.profile.deleteConfirm)) return;

    try {
      const response = await fetch(`http://localhost:8000/api/users/${userId}/posts/${postId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await loadPosts();
      }
    } catch (error) {
      console.error('Ошибка удаления:', error);
    }
  };

  const handleRebuildProfile = async () => {
    setRebuilding(true);
    try {
      const response = await fetch(`http://localhost:8000/api/users/${userId}/rebuild-profile`, {
        method: 'POST',
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Профиль перестроен! Проанализировано постов: ${data.total_posts}`);
      } else {
        const error = await response.json();
        alert(error.detail || 'Ошибка перестройки профиля');
      }
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Ошибка перестройки профиля');
    } finally {
      setRebuilding(false);
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'linkedin': return <Linkedin size={16} />;
      case 'instagram': return <Instagram size={16} />;
      case 'facebook': return <Facebook size={16} />;
      case 'telegram': return <MessageCircle size={16} />;
      default: return <FileText size={16} />;
    }
  };

  const platformStats = posts.reduce((acc, post) => {
    acc[post.platform] = (acc[post.platform] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="min-h-screen bg-white pt-32 pb-6 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onBack}
            className="mb-4 px-4 py-2 bg-white text-black text-sm font-black uppercase tracking-wide border-2 border-black hover:bg-[#ccff00] hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
          >
            ← {t.profile.back}
          </button>
          
          <div className="bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-3xl md:text-4xl font-black text-black uppercase tracking-tighter mb-2">
                  {userName}
                </h1>
                <p className="text-xs md:text-sm text-slate-600 font-bold">
                  ID: {userId.slice(0, 8)}...
                </p>
              </div>
              <div className="w-12 h-12 md:w-16 md:h-16 bg-black rounded-none flex items-center justify-center text-white border-2 border-black">
                <User size={24} className="md:w-8 md:h-8" />
              </div>
            </div>

            {/* Stats */}
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-slate-100 border-2 border-black p-3">
                <div className="text-xl md:text-2xl font-black text-black">{posts.length}</div>
                <div className="text-[10px] md:text-xs font-bold text-slate-600 uppercase">{t.profile.posts}</div>
              </div>
              {Object.entries(platformStats).map(([platform, count]) => (
                <div key={platform} className="bg-slate-100 border-2 border-black p-3">
                  <div className="text-xl md:text-2xl font-black text-black">{count}</div>
                  <div className="text-[10px] md:text-xs font-bold text-slate-600 uppercase flex items-center gap-1">
                    {getPlatformIcon(platform)}
                    {platform}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="mb-6 flex flex-col sm:flex-row gap-3">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 md:px-6 py-2 md:py-3 bg-black text-white text-xs md:text-sm font-black uppercase tracking-wide border-2 border-black transition-all hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_#ccff00] active:translate-y-0 active:shadow-none flex items-center justify-center gap-2"
          >
            <Plus size={16} className="md:w-[18px] md:h-[18px]" />
            <span>{t.profile.addPost}</span>
          </button>
          
          <button
            onClick={handleRebuildProfile}
            disabled={rebuilding || posts.length === 0}
            className="px-4 md:px-6 py-2 md:py-3 bg-white text-black text-xs md:text-sm font-black uppercase tracking-wide border-2 border-black transition-all hover:bg-[#ccff00] hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {rebuilding ? (
              <>
                <Loader2 size={16} className="md:w-[18px] md:h-[18px] animate-spin" />
                <span>{t.profile.rebuilding}</span>
              </>
            ) : (
              <>
                <RefreshCw size={16} className="md:w-[18px] md:h-[18px]" />
                <span>{t.profile.rebuild}</span>
              </>
            )}
          </button>
        </div>

        {/* Add Post Form */}
        {showAddForm && (
          <div className="mb-6 bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-4 md:p-6">
            <h2 className="text-lg md:text-xl font-black text-black uppercase tracking-tighter mb-4">
              {t.profile.newPost}
            </h2>
            
            <form onSubmit={handleAddPost} className="space-y-4">
              {/* Platform */}
              <div>
                <label className="block text-[10px] md:text-xs font-black text-black uppercase tracking-wider mb-2">
                  {t.profile.platform}
                </label>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value as any)}
                  className="w-full px-3 md:px-4 py-2 md:py-3 border-2 border-black bg-white text-sm md:text-base text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all"
                >
                  <option value="linkedin">LinkedIn</option>
                  <option value="instagram">Instagram</option>
                  <option value="facebook">Facebook</option>
                  <option value="telegram">Telegram</option>
                </select>
              </div>

              {/* Content */}
              <div>
                <label className="block text-[10px] md:text-xs font-black text-black uppercase tracking-wider mb-2">
                  {t.profile.content}
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={6}
                  className="w-full px-3 md:px-4 py-2 md:py-3 border-2 border-black bg-white text-sm md:text-base text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all resize-none"
                  placeholder={t.profile.content}
                  required
                />
              </div>

              {/* Hashtags */}
              <div>
                <label className="block text-[10px] md:text-xs font-black text-black uppercase tracking-wider mb-2">
                  {t.profile.hashtags}
                </label>
                <input
                  type="text"
                  value={hashtags}
                  onChange={(e) => setHashtags(e.target.value)}
                  className="w-full px-3 md:px-4 py-2 md:py-3 border-2 border-black bg-white text-sm md:text-base text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all"
                  placeholder="#leadership, #teamwork"
                />
              </div>

              {/* Emojis */}
              <div>
                <label className="block text-[10px] md:text-xs font-black text-black uppercase tracking-wider mb-2">
                  {t.profile.emojis}
                </label>
                <input
                  type="text"
                  value={emojis}
                  onChange={(e) => setEmojis(e.target.value)}
                  className="w-full px-3 md:px-4 py-2 md:py-3 border-2 border-black bg-white text-sm md:text-base text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all"
                  placeholder="🔥✨🚀"
                />
              </div>

              {/* Submit */}
              <div className="flex flex-col sm:flex-row gap-3">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 px-4 md:px-6 py-2 md:py-3 bg-black text-white text-xs md:text-sm font-black uppercase tracking-wide border-2 border-black transition-all hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_#ccff00] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {submitting ? (
                    <>
                      <Loader2 size={16} className="md:w-[18px] md:h-[18px] animate-spin" />
                      <span>{t.profile.adding}</span>
                    </>
                  ) : (
                    <>
                      <Check size={16} className="md:w-[18px] md:h-[18px]" />
                      <span>{t.profile.add}</span>
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddForm(false);
                    setContent('');
                    setHashtags('');
                    setEmojis('');
                  }}
                  className="flex-1 px-4 md:px-6 py-2 md:py-3 bg-white text-black text-xs md:text-sm font-black uppercase tracking-wide border-2 border-black transition-all hover:bg-red-50 hover:border-red-500 flex items-center justify-center gap-2"
                >
                  <X size={16} className="md:w-[18px] md:h-[18px]" />
                  <span>{t.profile.cancel}</span>
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Posts List */}
        <div className="bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
          <div className="p-3 md:p-4 border-b-2 border-black bg-white">
            <h2 className="text-lg md:text-xl font-black text-black uppercase tracking-tighter">
              {t.profile.myPosts} ({posts.length})
            </h2>
          </div>

          <div className="p-3 md:p-4 space-y-3 md:space-y-4">
            {loading ? (
              <div className="flex items-center justify-center p-8">
                <Loader2 className="w-8 h-8 animate-spin text-black" />
              </div>
            ) : posts.length === 0 ? (
              <div className="text-center p-8 text-sm md:text-base text-slate-600 font-bold">
                {t.profile.noPosts}
              </div>
            ) : (
              posts.map((post) => (
                <div
                  key={post.id}
                  className="bg-slate-50 border-2 border-black p-3 md:p-4 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
                >
                  <div className="flex items-start justify-between mb-2 md:mb-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      {getPlatformIcon(post.platform)}
                      <span className="text-[10px] md:text-xs font-black text-black uppercase">
                        {post.platform}
                      </span>
                      <span className="text-[10px] md:text-xs text-slate-500">
                        {new Date(post.timestamp).toLocaleDateString('ru-RU')}
                      </span>
                    </div>
                    <button
                      onClick={() => handleDeletePost(post.id)}
                      className="p-1.5 md:p-2 text-red-600 hover:bg-red-50 border-2 border-transparent hover:border-red-500 transition-all flex-shrink-0"
                    >
                      <Trash2 size={14} className="md:w-4 md:h-4" />
                    </button>
                  </div>
                  
                  <p className="text-xs md:text-sm text-black font-medium mb-2 whitespace-pre-wrap leading-relaxed">
                    {post.content}
                  </p>
                  
                  {(post.hashtags.length > 0 || post.emojis.length > 0) && (
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      {post.hashtags.map((tag, i) => (
                        <span key={i} className="text-[10px] md:text-xs font-bold text-blue-600">
                          {tag}
                        </span>
                      ))}
                      {post.emojis.map((emoji, i) => (
                        <span key={i} className="text-xs md:text-sm">
                          {emoji}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;

