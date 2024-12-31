using System;
using UnityEngine;
using System.Collections;
using UnityEngine.Tilemaps;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using Object = UnityEngine.Object;
using Random = UnityEngine.Random;
#if UNITY_EDITOR
using UnityEditor;
#endif

namespace HolyBlender
{
	public class GameManager : SingletonMonoBehaviour<GameManager>, ISaveableAndLoadable
	{
		public TemporaryActiveText notificationTemporaryActiveText;
		public static IUpdatable[] updatables = new IUpdatable[0];

		public override void Awake ()
		{
			base.Awake ();
#if !UNITY_WEBGL
			SaveAndLoadManager.Init ();
#endif
		}

		void Update ()
		{
			for (int i = 0; i < updatables.Length; i ++)
			{
				IUpdatable updatable = updatables[i];
				updatable.DoUpdate ();
			}
		}

		public void DisplayNotification (string text)
		{
			notificationTemporaryActiveText.text.text = text;
			notificationTemporaryActiveText.Do ();
		}

		public void Quit ()
		{
			Application.Quit();
		}

		void OnApplicationQuit ()
		{
			SaveAndLoadManager.Save ();
		}

		public static void DestroyImmediate (Object obj)
		{
			Object.DestroyImmediate(obj);
		}
		
#if UNITY_EDITOR
		public static void DestroyOnNextEditorUpdate (Object obj)
		{
			EditorApplication.update += () => { if (obj == null) return; DestroyObject (obj); };
		}

		static void DestroyObject (Object obj)
		{
			if (obj == null)
				return;
			EditorApplication.update -= () => { DestroyObject (obj); };
			DestroyImmediate(obj);
		}
#endif
	}
}