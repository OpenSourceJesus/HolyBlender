#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

namespace HolyBlender
{
	public class MeasureDistancesBetweenTransforms : EditorScript
	{
		[MenuItem("Tools/Print distance between selected objects")]
		static void _Do ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				for (int i2 = i + 1; i2 < selectedTransforms.Length; i2 ++)
				{
					Transform selectedTrs2 = selectedTransforms[i2];
					string output = Vector3.Distance(selectedTrs.position, selectedTrs2.position) + " is the distance between " + selectedTrs.name + " and " + selectedTrs2.name;
					output += "\n" + Mathf.Abs(selectedTrs.position.x - selectedTrs2.position.x) + " is the distance on the x-axis between " + selectedTrs.name + " and " + selectedTrs2.name;
					output += "\n" + Mathf.Abs(selectedTrs.position.y - selectedTrs2.position.y) + " is the distance on the y-axis between " + selectedTrs.name + " and " + selectedTrs2.name;
					output += "\n" + Mathf.Abs(selectedTrs.position.z - selectedTrs2.position.z) + " is the distance on the z-axis between " + selectedTrs.name + " and " + selectedTrs2.name;
					print(output);
				}
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class MeasureDistanceBetweenTransforms : EditorScript
	{
	}
}
#endif