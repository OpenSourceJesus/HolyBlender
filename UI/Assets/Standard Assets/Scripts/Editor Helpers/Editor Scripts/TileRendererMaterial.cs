using UnityEngine;

namespace HolyBlender
{
	public class TileRendererMaterial : EditorScript
	{
		public Transform trs;
		public Renderer renderer;
		public float multiplyTextureScale;
		public TileMethod tileMethod;
		public bool useRotation;

		public override void Do ()
		{
			if (this == null)
				return;
			if (trs == null)
				trs = GetComponent<Transform>();
			if (renderer == null)
				renderer = GetComponent<Renderer>();
			Vector3 lossyScale = trs.lossyScale;
			Vector2 textureScale = lossyScale;
			if (tileMethod == TileMethod.XZ)
				textureScale.y = lossyScale.z;
			else if (tileMethod == TileMethod.YZ)
				textureScale = new Vector2(lossyScale.y, lossyScale.z);
			else if (tileMethod == TileMethod.YX)
				textureScale = new Vector2(lossyScale.y, lossyScale.x);
			else if (tileMethod == TileMethod.ZX)
				textureScale = new Vector2(lossyScale.z, lossyScale.x);
			else if (tileMethod == TileMethod.ZY)
				textureScale = new Vector2(lossyScale.z, lossyScale.y);
			else if (tileMethod == TileMethod.XX)
				textureScale = new Vector2(lossyScale.x, lossyScale.x);
			else if (tileMethod == TileMethod.YY)
				textureScale = new Vector2(lossyScale.y, lossyScale.y);
			else if (tileMethod == TileMethod.ZZ)
				textureScale = new Vector2(lossyScale.z, lossyScale.z);
			Material material = new Material(renderer.sharedMaterial);
			if (useRotation)
				material.mainTextureScale = trs.rotation * textureScale * multiplyTextureScale;
			else
				material.mainTextureScale = textureScale * multiplyTextureScale;
			renderer.sharedMaterial = material;
		}

		public enum TileMethod
		{
			XY,
			XZ,
			YZ,
			YX,
			ZX,
			ZY,
			XX,
			YY,
			ZZ
		}
	}
}