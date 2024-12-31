using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class RectTransformExtensions
	{
		public static Rect GetWorldRect (this RectTransform rectTrs)
		{
			Vector2 min = rectTrs.TransformPoint(rectTrs.rect.min);
			Vector2 max = rectTrs.TransformPoint(rectTrs.rect.max);
			return Rect.MinMaxRect(min.x, min.y, max.x, max.y);
		}

		public static Bounds GetWorldBounds (this RectTransform rectTrs)
		{
			Vector3 min = rectTrs.TransformPoint(rectTrs.rect.min);
			Vector3 max = rectTrs.TransformPoint(rectTrs.rect.max);
			Bounds output = new Bounds();
			output.SetMinMax(min, max);
			return output;
		}
		
		public static Vector2 GetCenterInCanvasNormalized (this RectTransform rectTrs, RectTransform canvasRectTrs)
		{
			return canvasRectTrs.GetWorldRect().ToNormalizedPosition(rectTrs.GetWorldRect().center);
		}

		public static Rect GetRectInCanvasNormalized (this RectTransform rectTrs, RectTransform canvasRectTrs)
		{
			Rect output = rectTrs.GetWorldRect();
			Rect canvasRect = canvasRectTrs.GetWorldRect();
			Vector2 outputMin = canvasRect.ToNormalizedPosition(output.min);
			Vector2 outputMax = canvasRect.ToNormalizedPosition(output.max);
			return Rect.MinMaxRect(outputMin.x, outputMin.y, outputMax.x, outputMax.y);
		}

		public static void SetAnchorsToRect (this RectTransform rectTrs)
		{
			Rect parentRect = ((RectTransform) rectTrs.parent).GetWorldRect();
			Rect rect = rectTrs.GetWorldRect();
			Vector2 previousLocalPosition = rectTrs.localPosition;
			Vector2 previousSizeDelta = rectTrs.sizeDelta;
			rectTrs.anchorMin = parentRect.ToNormalizedPosition(rect.min);
			rectTrs.anchorMax = parentRect.ToNormalizedPosition(rect.max);
			rectTrs.SetSizeWithCurrentAnchors(RectTransform.Axis.Horizontal, previousSizeDelta.x);
			rectTrs.SetSizeWithCurrentAnchors(RectTransform.Axis.Vertical, previousSizeDelta.y);
			rectTrs.localPosition = previousLocalPosition;
		}
	}
}