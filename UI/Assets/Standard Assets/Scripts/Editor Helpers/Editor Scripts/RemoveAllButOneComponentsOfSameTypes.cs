#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

namespace HolyBlender
{
	public class RemoveAllButOneComponentsOfSameTypes : EditorScript
	{
		public GameObject go;

		public override void Do ()
		{
			if (this == null)
				return;
			if (go == null)
				go = gameObject;
			_Do (go);
		}

		static void _Do (GameObject go)
		{
			Component[] components = go.GetComponents<Component>();
			for (int i = 0; i < components.Length; i ++)
			{
				Component component = components[i];
				for (int i2 = i + 1; i2 < components.Length; i2 ++)
				{
					Component component2 = components[i2];
					if (component.GetType() == component2.GetType())
						GameManager.DestroyOnNextEditorUpdate (component2);
				}
			}
		}

		[MenuItem("Tools/Remove all but one components of same types on selected GameObjects")]
		static void _Do ()
		{
			GameObject[] selectedGos = Selection.gameObjects;
			for (int i = 0; i < selectedGos.Length; i ++)
			{
				GameObject selectedGo = selectedGos[i];
				_Do (selectedGo);
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class RemoveAllButOneComponentsOfSameTypes : EditorScript
	{
	}
}
#endif