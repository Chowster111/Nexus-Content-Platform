// services/likesClient.ts
import axios from 'axios'
import * as Sentry from '@sentry/react'
import type { LikedItem } from '../pages/Home'

const API_BASE = '/api'

/**
 * Retry helper with exponential backoff.
 * @param fn - The async function to retry.
 * @param retries - Max retries.
 * @param backoff - Initial backoff time in ms.
 */
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  retries = 3,
  backoff = 500
): Promise<T> {
  try {
    return await fn()
  } catch (err) {
    if (retries === 0) {
      console.error('❌ Max retries reached:', err)
      Sentry.captureException(err)
      throw err
    }
    console.warn(`⚠️ Retry attempt: ${4 - retries} | Waiting ${backoff}ms`)
    await new Promise((r) => setTimeout(r, backoff))
    return retryWithBackoff(fn, retries - 1, backoff * 2)
  }
}

export async function saveUserLikes(userId: string, likes: LikedItem[]) {
  const payload = {
    user_id: userId,
    likes: likes.map((item) => ({
      url: item.url,
      liked: item.liked,
    })),
  }

  return retryWithBackoff(async () => {
    await axios.post(`${API_BASE}/user/likes`, payload)
    console.log(`✅ Likes saved for user ${userId}`)
  })
}
