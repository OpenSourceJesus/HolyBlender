#if UNITY_EDITOR
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using Extensions;
using UnityEditor;

namespace HolyBlender
{
	public class SplitTransformAcrossItsBounds : EditorScript
	{
		public Vector3 splitInterval = Vector3.one;
		public BoundsOffset splitOffset;
		public Transform trs;

		public override void Do ()
		{
			if (trs == null)
				trs = GetComponent<Transform>();
			_Do (trs, splitInterval, splitOffset);
		}

		static void _Do (Transform trs, Vector3 splitInterval, BoundsOffset splitOffset)
		{
			Bounds bounds = trs.GetBounds().ToBoundsInt(MathfExtensions.RoundingMethod.HalfOrMoreRoundsUp, MathfExtensions.RoundingMethod.HalfOrLessRoundsDown).ToBounds().MakePositiveSize();
			Vector3[] pointsInside = bounds.GetPointsInside(splitInterval, splitOffset);
			trs.position = pointsInside[0] + Vector3.one / 2;
			trs.SetWorldScale (splitInterval);
			for (int i = 1; i < pointsInside.Length; i ++)
			{
				Vector3 pointInside = pointsInside[i] + Vector3.one / 2;
				Instantiate(trs, pointInside, trs.rotation, trs.parent);
			}
		}

		[MenuItem("Tools/Split selected objects across transform bounds")]
		static void _Do ()
		{
			Transform[] selectedTransforms = Selection.transforms;
			for (int i = 0; i < selectedTransforms.Length; i ++)
			{
				Transform selectedTrs = selectedTransforms[i];
				_Do (selectedTrs, Vector3.one, new BoundsOffset(Vector3.one / 2, Vector3.zero));
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class SplitTransformAcrossItsBounds : EditorScript
	{
	}
}
#endif