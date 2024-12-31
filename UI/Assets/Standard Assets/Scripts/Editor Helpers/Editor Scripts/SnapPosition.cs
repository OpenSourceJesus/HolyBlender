using UnityEngine;
using System.Collections;
using Extensions;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class SnapPosition : EditorScript
	{
		public bool useLocalPosition;
		public Transform trs;
		public Vector3 snapTo;
		public Vector3 offset;
		Vector3 newPosition;
		
		public override void Do ()
		{
			if (this == null)
				return;
			if (trs == null)
				trs = GetComponent<Transform>();
			if (!useLocalPosition)
			{
				newPosition = trs.position.Snap(snapTo);
				if (snapTo.x == 0)
					newPosition.x = trs.position.x;
				if (snapTo.y == 0)
					newPosition.y = trs.position.y;
				if (snapTo.z == 0)
					newPosition.z = trs.position.z;
				trs.position = newPosition + offset;
			}
			else
			{
				newPosition = trs.localPosition.Snap(snapTo);
				if (snapTo.x == 0)
					newPosition.x = trs.localPosition.x;
				if (snapTo.y == 0)
					newPosition.y = trs.localPosition.y;
				if (snapTo.z == 0)
					newPosition.z = trs.localPosition.z;
				trs.localPosition = newPosition + offset;
			}
		}
	}
}