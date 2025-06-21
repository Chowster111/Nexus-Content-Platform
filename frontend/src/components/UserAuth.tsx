import { useState, useEffect } from 'react'
import { supabase } from '../../lib/supabaseClient'
import type { User } from '@supabase/supabase-js'
import styles from '../styles/UserAuth.module.css'

export default function UserAuth() {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setUser(data?.session?.user ?? null)
    })

    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => {
      listener?.subscription.unsubscribe()
    }
  }, [])

  const signInWith = async (provider: 'google' | 'github') => {
    await supabase.auth.signInWithOAuth({ provider })
  }

  const signOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <div className={styles.authWrapper}>
      <div className={styles.authInner}>
        {user ? (
          <>
            <span className={styles.avatar}>👤</span>
            <span className={styles.email}>{user.email}</span>
            <button className={styles.iconButton} onClick={signOut} title="Sign Out">
              <img src="/icons/logout.svg" alt="Sign out" />
            </button>
          </>
        ) : (
          <>
            <button className={styles.iconButton} onClick={() => signInWith('google')} title="Sign in with Google">
              <img src="/icons/google.svg" alt="Google" />
            </button>
            <button className={styles.iconButton} onClick={() => signInWith('github')} title="Sign in with GitHub">
              <img src="/icons/github.svg" alt="GitHub" />
            </button>
          </>
        )}
      </div>
    </div>
  )
}
