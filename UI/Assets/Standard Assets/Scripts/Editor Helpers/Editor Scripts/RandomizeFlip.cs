#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class RandomizeFlip : EditorScript
	{
		public Transform trs;
		public bool canFlipX;
		public bool canFlipY;
		public bool canFlipZ;

		public override void Do ()
		{
			if (trs == null)
				trs = transform;
			if (canFlipX && Random.value < 0.5f)
				trs.localScale = trs.localScale.Multiply(new Vector3(-1, 1, 1));
			if (canFlipY && Random.value < 0.5f)
				trs.localScale = trs.localScale.Multiply(new Vector3(1, -1, 1));
			if (canFlipZ && Random.value < 0.5f)
				trs.localScale = trs.localScale.Multiply(new Vector3(1, 1, -1));
		}
	}
}
#else
namespace HolyBlender
{
	public class RandomizeFlip : EditorScript
	{
	}
}
#endif