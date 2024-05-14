#include "Prefab.h"
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Internationalization/Text.h"

APrefab::APrefab ()
{
}

APrefab::APrefab (FString assetPath)
{
	this->assetPath = assetPath;
}