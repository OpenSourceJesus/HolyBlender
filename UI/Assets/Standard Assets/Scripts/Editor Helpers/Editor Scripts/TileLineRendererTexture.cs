#if UNITY_EDITOR
using UnityEngine;

namespace HolyBlender
{
	public class TileLineRendererTexture : EditorScript
	{
		public LineRenderer lineRenderer;

		public override void Do ()
		{
			if (lineRenderer == null)
				lineRenderer = GetComponent<LineRenderer>();
			float textureAspectRatio = (float) lineRenderer.sharedMaterial.mainTexture.width / lineRenderer.sharedMaterial.mainTexture.height;
			float lineLength = lineRenderer.GetPosition(1).magnitude;
			float lineAspectRatio = lineLength / lineRenderer.startWidth;
			lineRenderer.textureScale = new Vector2(lineAspectRatio / textureAspectRatio / lineLength, 1);
		}
	}
}
#else
namespace HolyBlender
{
	public class TileLineRendererTexture : EditorScript
	{
	}
}
#endif