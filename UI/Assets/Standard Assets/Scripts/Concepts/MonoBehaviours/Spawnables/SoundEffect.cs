using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Extensions;
using System;

namespace HolyBlender
{
	public class SoundEffect : Spawnable
	{
		public AudioSource audioSource;
		public Settings settings = new Settings();
		
		public virtual void Play ()
		{
			audioSource.clip = settings.audioClip;
			audioSource.volume = settings.Volume;
			audioSource.maxDistance = settings.MaxDistance;
			audioSource.minDistance = settings.MinDistance;
			audioSource.Play();
			if (settings.persistant)
				DontDestroyOnLoad(gameObject);
			Destroy(gameObject, audioSource.clip.length);
		}
		
		[Serializable]
		public class Settings
		{
			public AudioClip audioClip;
			public bool persistant;
			float? volume;
			public float Volume
			{
				get
				{
					if (volume == null)
						return AudioManager.Instance.soundEffectPrefab.audioSource.volume;
					else
						return (float) volume;
				}
				set
				{
					volume = value;
				}
			}
			float? maxDistance;
			public float MaxDistance
			{
				get
				{
					if (maxDistance == null)
						return AudioManager.Instance.soundEffectPrefab.audioSource.maxDistance;
					else
						return (float) maxDistance;
				}
				set
				{
					maxDistance = value;
				}
			}
			float? minDistance;
			public float MinDistance
			{
				get
				{
					if (minDistance == null)
						return AudioManager.Instance.soundEffectPrefab.audioSource.minDistance;
					else
						return (float) minDistance;
				}
				set
				{
					minDistance = value;
				}
			}
			public Transform speakerTrs;
			Vector3? position;
			public Vector3 Position
			{
				get
				{
					if (speakerTrs != null)
						return speakerTrs.position;
					else
					{
						if (position == null)
							return AudioManager.Instance.soundEffectPrefab.trs.position;
						else
							return (Vector3) position;
					}
				}
				set
				{
					position = value;
				}
			}
			Quaternion? rotation;
			public Quaternion Rotation
			{
				get
				{
					if (speakerTrs != null)
						return speakerTrs.rotation;
					else
					{
						if (rotation == null)
							return AudioManager.Instance.soundEffectPrefab.trs.rotation;
						else
							return (Quaternion) rotation;
					}
				}
				set
				{
					rotation = value;
				}
			}
		}
	}
}