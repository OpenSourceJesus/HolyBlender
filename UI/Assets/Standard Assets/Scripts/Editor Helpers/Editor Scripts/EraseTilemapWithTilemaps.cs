#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using UnityEditor;
using UnityEngine.Tilemaps;

namespace HolyBlender
{
	public class EraseTilemapWithTilemaps : EditorScript
	{
		public Tilemap[] eraseWithTilemaps = new Tilemap[0];
		public Tilemap eraseTilemap;
		public bool canEraseAtAnyTile = true;
		public TileBase[] tilesToEraseAt = new TileBase[0];
		public bool canEraseAnyTile = true;
		public TileBase[] erasableTiles = new TileBase[0];

		public override void Do ()
		{
			BoundsInt[] boundsArray = new BoundsInt[eraseWithTilemaps.Length];
			for (int i = 0; i < eraseWithTilemaps.Length; i ++)
			{
				Tilemap tilemap = eraseWithTilemaps[i];
				tilemap.CompressBounds();
				boundsArray[i] = tilemap.cellBounds;
			}
			BoundsInt cellBounds = boundsArray.Combine();
			foreach (Vector3Int cellPosition in cellBounds.allPositionsWithin)
			{
				for (int i = 0; i < eraseWithTilemaps.Length; i ++)
				{
					Tilemap tilemap = eraseWithTilemaps[i];
					TileBase tile = tilemap.GetTile(cellPosition);
					if (tile != null && (canEraseAtAnyTile || tilesToEraseAt.Contains(tile)))
					{
						TileBase tileToErase = eraseTilemap.GetTile(cellPosition);
						if (canEraseAnyTile || erasableTiles.Contains(tileToErase))
							eraseTilemap.SetTile(cellPosition, null);
					}
				}
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class EraseTilemapWithTilemaps : EditorScript
	{
	}
}
#endif