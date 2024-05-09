// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Prefab.h"
#include "ꗈ0.generated.h"

UCLASS()
class BAREUEPROJECT_API ꗈ1 : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ꗈ1();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;
	FVector2D GetMousePosition ();
	FVector ScreenToWorldPoint (FVector2D screenPoint);
	FVector GetMousePositionWorld ();
	float GetFacingAngle (FVector v);
	AActor* SpawnActor (AActor actor, FVector position, FRotator rotation);
};