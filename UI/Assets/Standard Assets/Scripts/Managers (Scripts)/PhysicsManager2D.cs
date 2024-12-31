using System;
using System.Collections.Generic;

public class PhysicsManager2D : SingletonMonoBehaviour<PhysicsManager2D>
{
	public LayerCollision[] layerCollisions = new LayerCollision[0];
	public static Dictionary<string, string[]> layerCollisionsDict = new Dictionary<string, string[]>();

	public override void Awake ()
	{
		base.Awake ();
		layerCollisionsDict.Clear();
		for (int i = 0; i < layerCollisions.Length; i ++)
		{
			LayerCollision layerCollision = layerCollisions[i];
			layerCollisionsDict.Add(layerCollision.layerName, layerCollision.collidingLayers);
		}
	}

	[Serializable]
	public struct LayerCollision
	{
		public string layerName;
		public string[] collidingLayers;
	}
}