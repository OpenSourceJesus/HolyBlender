#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class RandomizeSize : EditorScript
	{
		public Transform trs;
		public FloatRange range;

		public override void Do ()
		{
			if (trs == null)
				trs = transform;
			trs.localScale = Vector3.one * range.Get(Random.value);
		}
	}
}
#else
namespace HolyBlender
{
	public class RandomizeSize : EditorScript
	{
	}
}
#endif