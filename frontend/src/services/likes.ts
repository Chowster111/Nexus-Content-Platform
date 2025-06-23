// services/likes.ts
import axios from 'axios'
import type { LikedItem } from '../App'

const API_BASE = '/api'

export async function saveUserLikes(userId: string, likes: LikedItem[]) {
  try {
    await axios.post(`${API_BASE}/user/likes`, {
    user_id: userId,
    likes: likes.map((item) => ({
        url: item.url,
        liked: item.liked,
    })),
    })
    console.log('✅ Likes saved successfully.')
  } catch (error) {
    console.error('❌ Error saving likes:', error)
    throw error
  }
}
