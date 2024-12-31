#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using Extensions;

namespace HolyBlender
{
	public class SetRectTransformAnchorsToRect : EditorScript
	{
		public RectTransform rectTrs;

		public override void Do ()
		{
			if (rectTrs == null)
				rectTrs = GetComponent<RectTransform>();
			_Do (rectTrs);
		}

		static void _Do (RectTransform rectTrs)
		{
			rectTrs.SetAnchorsToRect ();
		}
		
		[MenuItem("Tools/Set selected RectTransforms' anchors to rects")]
		static void _Do ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				RectTransform selectedRectTrs = selectedTrs as RectTransform;
				if (selectedRectTrs != null)
					_Do (selectedRectTrs);
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class SetRectTransformAnchorsToRect : EditorScript
	{
	}
}
#endif