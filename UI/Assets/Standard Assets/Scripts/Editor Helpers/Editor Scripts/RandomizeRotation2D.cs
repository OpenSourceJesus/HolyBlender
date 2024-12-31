#if UNITY_EDITOR
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class RandomizeRotation2D : EditorScript
	{
		public Transform trs;

		public override void Do ()
		{
			if (trs == null)
				trs = transform;
			trs.eulerAngles = Vector3.forward * Random.value * 360;
		}
	}
}
#else
namespace HolyBlender
{
	public class RandomizeRotation2D : EditorScript
	{
	}
}
#endif