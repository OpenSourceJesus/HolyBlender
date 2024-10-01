using UnityEngine;

[ExecuteInEditMode]
public class LoadSprite : MonoBehaviour
{
	public string spritePath;

	void Start ()
	{
		GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>(spritePath);
	}
}