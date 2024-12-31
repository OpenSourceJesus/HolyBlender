#if UNITY_EDITOR
using UnityEngine;

namespace HolyBlender
{
	public class SetAudioSourcePitchForDuration : EditorScript
	{
        public AudioSource audioSource;
        public float duration;

		public override void Do ()
		{
			if (audioSource == null)
				audioSource = GetComponent<AudioSource>();
            _Do (audioSource, duration);
		}

        public static void _Do (AudioSource audioSource, float duration)
        {
            audioSource.pitch = audioSource.clip.length / duration;
        }
	}
}
#else
namespace HolyBlender
{
	public class SetAudioSourcePitchForDuration : EditorScript
	{
	}
}
#endif