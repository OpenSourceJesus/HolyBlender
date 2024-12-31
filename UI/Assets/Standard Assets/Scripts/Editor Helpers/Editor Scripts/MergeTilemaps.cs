#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using UnityEditor;
using UnityEngine.Tilemaps;

namespace HolyBlender
{
	public class MergeTilemaps : EditorScript
	{
		public Tilemap[] from = new Tilemap[0];
		public Tilemap to;

		public override void Do ()
		{
			for (int i = 0; i < from.Length; i ++)
			{
				Tilemap tilemap = from[i];
				foreach (Vector3Int cellPosition in tilemap.cellBounds.allPositionsWithin)
				{
					TileBase tile = tilemap.GetTile(cellPosition);
					if (tile != null)
						to.SetTile(cellPosition, tile);
				}
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class MergeTilemaps : EditorScript
	{
	}
}
#endif