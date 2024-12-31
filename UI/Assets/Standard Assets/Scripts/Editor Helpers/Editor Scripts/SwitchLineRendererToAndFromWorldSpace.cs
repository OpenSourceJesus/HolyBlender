using UnityEngine;

namespace HolyBlender
{
	public class SwitchLineRendererToAndFromWorldSpace : EditorScript
	{
		public LineRenderer lineRenderer;
		public Transform trs;

		public override void Do ()
		{
			if (lineRenderer == null)
				lineRenderer = GetComponent<LineRenderer>();
			if (trs == null)
				trs = GetComponent<Transform>();
			Vector3[] positions = new Vector3[lineRenderer.positionCount];
			lineRenderer.GetPositions(positions);
			for (int i = 0; i < lineRenderer.positionCount; i ++)
			{
				Vector3 position = positions[i];
				if (lineRenderer.useWorldSpace)
					positions[i] = trs.InverseTransformPoint(position);
				else
					positions[i] = trs.TransformPoint(position);
			}
			lineRenderer.SetPositions(positions);
			lineRenderer.useWorldSpace = !lineRenderer.useWorldSpace;
		}
	}
}