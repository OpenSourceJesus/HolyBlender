﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Extensions;

namespace HolyBlender
{
	public class AudioManager : SingletonMonoBehaviour<AudioManager>
	{
		public float Volume
		{
			get
			{
				return PlayerPrefs.GetFloat("Volume", 1);
			}
			set
			{
				AudioListener.volume = value;
				PlayerPrefs.SetFloat("Volume", value);
			}
		}
		public bool Mute
		{
			get
			{
				return PlayerPrefsExtensions.GetBool("Mute");
			}
			set
			{
				AudioListener.pause = value;
				PlayerPrefsExtensions.SetBool("Mute", value);
			}
		}
		public SoundEffect soundEffectPrefab;
		
		public SoundEffect MakeSoundEffect (AudioClip audioClip, Vector3 position)
		{
			return MakeSoundEffect(audioClip, position, soundEffectPrefab.settings.Volume);
		}
		
		public SoundEffect MakeSoundEffect (AudioClip audioClip, Vector3 position, float volume)
		{
			SoundEffect.Settings soundEffectSettings = soundEffectPrefab.settings;
			soundEffectSettings.audioClip = audioClip;
			soundEffectSettings.Position = position;
			soundEffectSettings.Volume = volume;
			return MakeSoundEffect(soundEffectSettings);
		}
		
		public SoundEffect MakeSoundEffect (SoundEffect.Settings soundEffectSettings)
		{
			SoundEffect output = ObjectPool.instance.SpawnComponent<SoundEffect>(soundEffectPrefab.prefabIndex, soundEffectSettings.Position, soundEffectSettings.Rotation);
			output.settings = soundEffectSettings;
			output.Play();
			return output;
		}
	}
}