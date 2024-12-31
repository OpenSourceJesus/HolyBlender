#if UNITY_EDITOR
using UnityEngine;
using UnityEngine.UI;

namespace HolyBlender
{
	public class SetImageRectTransformToSpriteRect : EditorScript
	{
		public Image image;
		public RectTransform rectTrs;

		public override void Do ()
		{
			if (image == null)
				image = GetComponent<Image>();
			if (rectTrs == null)
				rectTrs = image.rectTransform;
			Rect spriteRect = image.sprite.rect;
			rectTrs.SetInsetAndSizeFromParentEdge(RectTransform.Edge.Left, spriteRect.min.x, spriteRect.size.x);
			rectTrs.SetInsetAndSizeFromParentEdge(RectTransform.Edge.Bottom, spriteRect.min.y, spriteRect.size.y);
		}
	}
}
#else
namespace HolyBlender
{
	public class SetImageRectTransformToSpriteRect : EditorScript
	{
	}
}
#endif
