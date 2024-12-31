using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[ExecuteInEditMode]
public class WebRenderer2D : MonoBehaviour
{
	public bool autoSetLineRenderers;
	public Transform lineRenderersParent;
	public Transform pointsParent;
	public Transform[] points = new Transform[0];
	public bool autoSetRegionCount;
	public Region[] regions = new Region[0];
    public bool update;
	int indexOfNullPoint;
	LineRenderer[] lineRenderers;

    void OnValidate ()
    {
        if (update)
        {
            update = false;
            DoUpdate ();
        }
    }

	public virtual void DoUpdate ()
	{
		if (autoSetRegionCount)
		{
			lineRenderers = lineRenderersParent.GetComponentsInChildren<LineRenderer>();
			Region region;
			if (regions.Length < lineRenderers.Length)
			{
				for (int i = regions.Length; i < lineRenderers.Length; i ++)
				{
					region = new Region();
					region.lineRenderer = lineRenderers[i];
					region.autoSetPositions = true;
					regions = regions.Add(region);
				}
			}
		}
		if (autoSetLineRenderers)
		{
			lineRenderers = lineRenderersParent.GetComponentsInChildren<LineRenderer>();
			for (int i = 0; i < regions.Length; i ++)
				regions[i].lineRenderer = lineRenderers[i];
		}
		while (true)
		{
			indexOfNullPoint = points.IndexOf(null);
			if (indexOfNullPoint == -1)
				break;
			else
				points = points.RemoveAt(indexOfNullPoint);
		}
		foreach (Region region in regions)
		{
			if (region.autoSetPositions)
			{
				for (int i = 0; i < region.lineRenderer.positionCount; i ++)
					region.lineRenderer.SetPosition(i, TransformExtensions.GetClosestTransform_2D(points, region.lineRenderer.GetPosition(i)).position);
			}
		}
	}

	[Serializable]
	public class Region
	{
		public LineRenderer lineRenderer;
		public bool autoSetPositions;
	}
}