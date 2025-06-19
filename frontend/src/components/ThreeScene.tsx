import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'
import styles from '../styles/ThreeScene.module.css'

const ThreeScene: React.FC = () => {
  const containerRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    let scene = new THREE.Scene()
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
    let renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })

    renderer.setSize(window.innerWidth, window.innerHeight)
    renderer.setClearColor(0x000000, 1)
    containerRef.current.appendChild(renderer.domElement)

    let raycaster = new THREE.Raycaster()
    let mouse = new THREE.Vector2()
    let boxes: THREE.LineSegments[] = []

    for (let i = 0; i < 20; i++) {
      const size = Math.random() * 1.5 + 0.8
      const geometry = new THREE.BoxGeometry(size, size, size)
      const edges = new THREE.EdgesGeometry(geometry)
      const opacity = 0.3 + Math.random() * 0.5
      const grayValue = Math.floor(100 + Math.random() * 156)
      const color = (grayValue << 16) | (grayValue << 8) | grayValue

      const material = new THREE.LineBasicMaterial({
        color: color,
        transparent: true,
        opacity: opacity,
      })

      const box = new THREE.LineSegments(edges, material)

      box.position.set(
        (Math.random() - 0.5) * 30,
        (Math.random() - 0.5) * 25,
        (Math.random() - 0.5) * 25
      )

      box.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        Math.random() * Math.PI
      )

      // @ts-ignore
      box.userData = {
        velocity: new THREE.Vector3(
          (Math.random() - 0.5) * 0.015,
          (Math.random() - 0.5) * 0.015,
          (Math.random() - 0.5) * 0.015
        ),
        rotationSpeed: new THREE.Vector3(
          (Math.random() - 0.5) * 0.015,
          (Math.random() - 0.5) * 0.015,
          (Math.random() - 0.5) * 0.015
        ),
        originalOpacity: opacity,
        pulseSpeed: 0.02 + Math.random() * 0.02,
        pulseOffset: Math.random() * Math.PI * 2,
      }

      scene.add(box)
      boxes.push(box)
    }

    camera.position.z = 15

    const onWindowResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight
      camera.updateProjectionMatrix()
      renderer.setSize(window.innerWidth, window.innerHeight)
    }

    window.addEventListener('resize', onWindowResize)

    const animate = () => {
      requestAnimationFrame(animate)
      const time = Date.now() * 0.001

      boxes.forEach((box) => {
        const userData = box.userData
        box.position.add(userData.velocity)
        box.rotation.x += userData.rotationSpeed.x
        box.rotation.y += userData.rotationSpeed.y
        box.rotation.z += userData.rotationSpeed.z

        const pulse = Math.sin(time * userData.pulseSpeed + userData.pulseOffset) * 0.2 + 0.8;
        (box.material as THREE.LineBasicMaterial).opacity = userData.originalOpacity * pulse

        // Bounce logic
        if (box.position.x > 20 || box.position.x < -20) userData.velocity.x *= -1
        if (box.position.y > 15 || box.position.y < -15) userData.velocity.y *= -1
        if (box.position.z > 15 || box.position.z < -15) userData.velocity.z *= -1
      })

      renderer.render(scene, camera)
    }

    animate()

    return () => {
      window.removeEventListener('resize', onWindowResize)
      containerRef.current?.removeChild(renderer.domElement)
      renderer.dispose()
    }
  }, [])

  return <div className={styles.threeContainer} ref={containerRef}></div>
}

export default ThreeScene
