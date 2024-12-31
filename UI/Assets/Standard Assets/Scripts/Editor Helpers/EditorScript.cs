#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System;
using UnityEngine.Events;
using Extensions;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class EditorScript : MonoBehaviour
	{
		public static InputEvent inputEvent = new InputEvent();
		public Hotkey[] hotkeys = new Hotkey[0];
		public bool doOnce;
		public bool doRepeatedly;

		public virtual void OnEnable ()
		{
			if (Application.isPlaying)
				EditorApplication.update -= Do;
		}

		public virtual void OnDisable ()
		{
			EditorApplication.update -= Do;
		}

		public virtual void OnDestroy ()
		{
			EditorApplication.update -= Do;
		}

		public virtual void OnValidate ()
		{
			if (doRepeatedly)
				EditorApplication.update += Do;
			else
				EditorApplication.update -= Do;
			if (!doOnce)
				return;
			doOnce = false;
			Do ();
		}
		
		public virtual void Do ()
		{
		}

		public virtual void UpdateHotkeys ()
		{
			if (Event.current == null)
				return;
			bool shouldBreak = false;
			inputEvent.mousePosition = Event.current.mousePosition.ToVec2Int();
			inputEvent.type = Event.current.type;
			for (int i = 0; i < hotkeys.Length; i ++)
			{
				Hotkey hotkey = hotkeys[i];
				foreach (Hotkey.Button button in hotkey.buttons)
				{
					if (Event.current.keyCode == button.key)
					{
						if (Event.current.type == EventType.KeyDown)
						{
							inputEvent.keys = inputEvent.keys.Add(Event.current.keyCode);
							button.isPressing = true;
							if (hotkey.downType == Hotkey.DownType.All)
							{
								foreach (Hotkey.Button button2 in hotkey.buttons)
								{
									if (!button2.isPressing)
									{
										shouldBreak = true;
										break;
									}
								}
								if (shouldBreak)
									break;
							}
							hotkey.downAction.Invoke();
						}
						else if (Event.current.type == EventType.KeyUp)
						{
							inputEvent.keys = inputEvent.keys.Remove(Event.current.keyCode);
							button.isPressing = false;
							if (hotkey.upType == Hotkey.UpType.All)
							{
								foreach (Hotkey.Button button2 in hotkey.buttons)
								{
									if (button2.isPressing)
									{
										shouldBreak = true;
										break;
									}
								}
								if (shouldBreak)
									break;
							}
							hotkey.upAction.Invoke();
						}
					}
				}
			}
		}

		public static Vector2Int GetMousePosition ()
		{
			return inputEvent.mousePosition;
		}

		public static Vector3 GetMousePositionInWorld ()
		{
			return GetSceneViewCamera().ScreenToWorldPoint(GetMousePosition().ToVec2());
		}

		public static Ray GetMouseRay ()
		{
			Camera camera = GetSceneViewCamera();
			Vector2 screenPoint = GetMousePosition();
			screenPoint.y = camera.pixelHeight - screenPoint.y;
			return camera.ScreenPointToRay(screenPoint);
		}

		public static Camera GetSceneViewCamera ()
		{
			Camera camera = SceneView.lastActiveSceneView.camera;
			if (camera == null)
				camera = SceneView.currentDrawingSceneView.camera;
			return camera;
		}

		[Serializable]
		public class Hotkey
		{
			public string name;
			public Button[] buttons;
			public DownType downType;
			public UpType upType;
			public UnityEvent downAction;
			public UnityEvent upAction;

			public enum DownType
			{
				All,
				// Any
			}

			public enum UpType
			{
				All,
				// Any
			}

			[Serializable]
			public class Button
			{
				public KeyCode key;
				public bool isPressing;
			}
		}

		public class InputEvent
		{
			public Vector2Int mousePosition;
			public EventType type;
			public KeyCode[] keys = new KeyCode[0];
		}
	}

	[CustomEditor(typeof(EditorScript))]
	public class EditorScriptEditor : Editor
	{
		public override void OnInspectorGUI ()
		{
			base.OnInspectorGUI ();
			EditorScript editorScript = (EditorScript) target;
			editorScript.UpdateHotkeys ();
		}

		public virtual void OnSceneGUI ()
		{
			EditorScript editorScript = (EditorScript) target;
			editorScript.UpdateHotkeys ();
		}
	}
}
#else
using UnityEngine;

namespace HolyBlender
{
	public class EditorScript : MonoBehaviour
	{
		public virtual void Do ()
		{
		}
	}
}
#endif