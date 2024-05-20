// Fill out your copyright notice in the Description page of Project Settings.


#include "ꗈ0.h"
#include <stdio.h>
ꗈ2
#include "Camera/PlayerCameraManager.h"
#include "Templates/SharedPointer.h"
#include "Utils.h"
#include "UObject/UObjectGlobals.h"
#include "Templates/Casts.h"
#include "UObject/SoftObjectPath.h"
#include <iostream>

// Sets default values
ꗈ1::ꗈ1()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;
}

// Called when the game starts or when spawned
void ꗈ1::BeginPlay()
{
	Super::BeginPlay();
	ꗈ3
	RegisterActorTickFunctions(true);
	RootComponent->SetMobility(EComponentMobility::Movable);
	APlayerController* playerController = GetWorld()->GetFirstPlayerController();
	if (IsValid(playerController))
	{
		APawn* pawn = playerController->GetPawnOrSpectator();
		if (IsValid(pawn))
		{
			// pawn->Destroy();
			pawn->DisableInput(playerController);
			APlayerCameraManager* cameraManager = playerController->PlayerCameraManager;
			pawn->TeleportTo(cameraManager->GetCameraLocation(), cameraManager->GetCameraRotation(), true, true);
		}
	}
}

// Called every frame
void ꗈ1::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	ꗈ4
}

AActor* ꗈ1::SpawnActor (FString assetPath, FVector location, FRotator rotation)
{
	FSoftObjectPath assetRef(assetPath);
	UBlueprint* blueprint = Cast<UBlueprint>(assetRef.TryLoad());
	FActorSpawnParameters spawnParameters;
	spawnParameters.Owner = this;
	spawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AActor* output = GetWorld()->SpawnActor(blueprint->GeneratedClass, TSharedPtr<const FVector>(&location).Get(), TSharedPtr<const FRotator>(&rotation).Get(), spawnParameters);
	return output;
}