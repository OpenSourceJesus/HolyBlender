#include "Prefab.h"
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "Internationalization/Text.h"

APrefab::APrefab ()
{
}

APrefab::APrefab (TMap<FString, FString> assetsPathsDict)
{
	this->assetsPathsDict = assetsPathsDict;
}