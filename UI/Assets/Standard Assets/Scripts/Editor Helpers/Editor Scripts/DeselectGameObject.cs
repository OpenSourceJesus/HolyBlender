#if UNITY_EDITOR
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using Extensions;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class DeselectGameObject : EditorScript
	{
		public GameObject go;

		public override void Do ()
		{
			_Do (go);
		}

		public static void _Do (GameObject go)
		{
			Selection.objects = Selection.objects.Remove(go);
		}

		[MenuItem("Tools/Deselect GameObjects with DeselectGameObject attached")]
		static void _Do ()
		{
			GameObject[] selectedGos = Selection.gameObjects;
			for (int i = 0; i < selectedGos.Length; i ++)
			{
				GameObject go = selectedGos[i];
				DeselectGameObject deselectGo = go.GetComponent<DeselectGameObject>();
				if (deselectGo != null)
					Selection.objects = Selection.objects.Remove(go);
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class DeselectObject : EditorScript
	{
	}
}
#endif