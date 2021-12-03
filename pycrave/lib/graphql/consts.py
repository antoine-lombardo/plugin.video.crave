# ===================================================================
#
#   HEADERS
#
# ===================================================================

HEADERS = {
  'accept': 'application/json',
  'accept-encoding': 'gzip',
  'connection': 'Keep-Alive',
  'content-type': 'application/json; charset=utf-8',
  'graphql-client-platform': 'entpay_android',
  'user-agent': 'okhttp/4.9.0'
}





# ===================================================================
#
#   CATEGORIES CONFIG
#
# ===================================================================

HOME_SCREEN = 'HOME'
ROOT_SCREENS = ['TV_SERIES', 'MOVIES']





# ===================================================================
#
#   PAYLOADS
#
# ===================================================================

SEARCH_PAYLOAD = {
  "operationName": "searchMedia",
  "variables": {
    "searchTerm": "TO FILL", # TO FILL
    "pageNumber": 0,
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "ENGLISH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH"
  },
  'query': 'query searchMedia($searchTerm: String!, $pageNumber: Int = 0, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext( maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { searchMedia(pageSize: 50, titleMatches: $searchTerm) { __typename page(page: $pageNumber) { __typename totalItemCount totalPageCount hasNextPage hasPreviousPage items { __typename ... BasicMediaPosterFragment } } } } fragment BasicMediaPosterFragment on AxisMedia { __typename id title axisId agvotCode flag { __typename title label } images(formats: [POSTER]) { __typename url } resourceCodes }'
}



MEDIA_PAYLOAD = {
  "operationName": "AxisMedia",
  "variables": {
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "ENGLISH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH",
    "id": "TO FILL", # TO FILL
    "imageFormat": [
      "THUMBNAIL",
      "THUMBNAIL_WIDE",
      "POSTER"
    ]
  },
  "query": "query AxisMedia($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!, $imageFormat: [ImageFormat]!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { axisMedia(id: $id) { __typename ...AxisMediaInfo seasons { __typename ...SeasonInfoFragment } promotionalContents(mode: NONE) { __typename page { __typename items { __typename ...AxisContentFragment } } } relatedCollections { __typename id axisCollectionItemCount title collection { __typename page { __typename totalItemCount items { __typename ...BasicMediaPosterFragment } } } } } } fragment AxisMediaInfo on AxisMedia { __typename ...AxisMediaBasicInfo mainContents { __typename page { __typename items { __typename ...AxisContentFragment } } } firstPlayableContent { __typename ...AxisContentFragment } featuredClip { __typename ...AxisContentFragment } normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } cast { __typename role castMembers { __typename fullName } } metadataUpgrade { __typename userIsSubscribed packageName subText languages } adUnit { __typename ... BasicAdUnitFragment } } fragment AxisMediaBasicInfo on AxisMedia { __typename id axisId title agvotCode qfrCode summary description mediaType originalSpokenLanguage mediaConstraint { __typename hasConstraintsNow } genres { __typename name } axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } images(formats: $imageFormat) { __typename ...ImageFragment } flag { __typename title label } firstAirYear ratingCodes resourceCodes heroBrandLogoId originatingNetworkLogoId } fragment AxisContentFragment on AxisContent { __typename id axisId title contentType axisMediaTitle summary description seasonNumber episodeNumber broadcastDate images(formats: $imageFormat) { __typename ...ImageFragment } axisMedia: axisMedia { __typename id axisId firstAirYear } duration durationSecs agvotCode axisPlaybackLanguages { __typename offlineDownload { __typename allowed } contentPackageId ...PlaybackLanguagesFragment } adUnit { __typename ...BasicAdUnitFragment } qfrCode ratingCodes videoPlayerDestCode originalSpokenLanguage normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } resourceCodes authConstraints { __typename ...AuthConstraintFragment } flag { __typename title label } } fragment ImageFragment on AxisImage { __typename format url } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } } fragment NormalizedRatingCodeFragment on NormalizedRatingCode { __typename language ratingCodes } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName } fragment SeasonInfoFragment on AxisSeason { __typename id axisId title seasonNumber resourceCodes axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } metadataUpgrade { __typename languages packageName userIsSubscribed } images(formats: [THUMBNAIL]) { __typename url } } fragment BasicMediaPosterFragment on AxisMedia { __typename id title axisId agvotCode flag { __typename title label } images(formats: [POSTER]) { __typename url } resourceCodes }"
}



SEASON_PAYLOAD = {
  "operationName": "axisSeason",
  "variables": {
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "FRENCH", # TO FILL
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH", # TO FILL
    "id": "TO FILL", # TO FILL
    "imageFormat": [
      "THUMBNAIL",
      "THUMBNAIL_WIDE",
      "POSTER"
    ]
  },
  "query": "query axisSeason($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!, $imageFormat:[ImageFormat]!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { axisSeason(id: $id) { __typename ...SeasonsFragment } } fragment SeasonsFragment on AxisSeason { __typename ...SeasonInfoFragment episodes { __typename ...EpisodeFragment } } fragment SeasonInfoFragment on AxisSeason { __typename id axisId title seasonNumber resourceCodes axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } metadataUpgrade { __typename languages packageName userIsSubscribed } images(formats: [THUMBNAIL]) { __typename url } } fragment EpisodeFragment on AxisContent { __typename broadcastDate seasonNumber episodeNumber ...AxisContentFragment } fragment AxisContentFragment on AxisContent { __typename id axisId title contentType axisMediaTitle summary description seasonNumber episodeNumber broadcastDate images(formats: $imageFormat) { __typename ...ImageFragment } axisMedia: axisMedia { __typename id axisId firstAirYear } duration durationSecs agvotCode axisPlaybackLanguages { __typename offlineDownload { __typename allowed } contentPackageId ...PlaybackLanguagesFragment } adUnit { __typename ...BasicAdUnitFragment } qfrCode ratingCodes videoPlayerDestCode originalSpokenLanguage normalizedRatingCodes { __typename ...NormalizedRatingCodeFragment } resourceCodes authConstraints { __typename ...AuthConstraintFragment } flag { __typename title label } } fragment ImageFragment on AxisImage { __typename format url } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } } fragment NormalizedRatingCodeFragment on NormalizedRatingCode { __typename language ratingCodes } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName }"
}



ROOT_SCREEN_PAYLOAD = {
  "operationName": "applicationScreens",
  "variables": {
    "appName": "contentid/app-mobile",
    "subscriptions": [],
    "maturity": "ADULT",
    "language": "FRENCH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH"
  },
  "query": "query applicationScreens($appName: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext( maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { app(id: $appName) { __typename title id splashScreen { __typename ...SplashOnboarding } corporateLinks { __typename ...LinkData } navigationLinks { __typename ...LinkData } screens { __typename ...AppScreen } iapElements { __typename id title platform } } } fragment SplashOnboarding on InfoSplashModal { __typename ctaText dismissButtonText id link { __typename ...LinkData } summary title image { __typename url } } fragment LinkData on Link { __typename title renderAs linkType url linkLabel internalContent { __typename title ... on Screen { id containerType screenCollectionType } } } fragment AppScreen on Screen { __typename screenCollectionType id }"
}



SCREEN_PAYLOAD = {
  "operationName": "screen",
  "variables": {
    "id": "",
    "subscriptions": [],
    "maturity": "ADULT",
    "language": "FRENCH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH"
  },
  "query": "query screen($id: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { screen(id: $id) { __typename id title screenCollectionType containerType adUnit { __typename ...AceBasicAdUnitFragment } collections { __typename id ...CollectionContainerInfoFragment ...RotatorInfoFragment ...AdElementInfoFragment ...GridInfoFragment ...MobileLinkFragment ...PromoElement ... on LinearVideo { title videoStreams { __typename ...VideoStreamInfoFragment } } } secondaryNavigation { __typename links { __typename ...MobileLinkFragment } renderTitleAs title titleImage { __typename url } } } } fragment AceBasicAdUnitFragment on AceAdUnit { __typename product heroBrand pageType revShare title adultAudience keyValue { __typename adTarget revShare pageTitle mediaType contentType } } fragment CollectionContainerInfoFragment on CollectionContainer { __typename collection { __typename page { __typename totalItemCount } } collectionAttributes { __typename subType options { __typename mediaTypes genres keywords } } } fragment RotatorInfoFragment on Rotator { __typename id title axisCollectionId config { __typename style ...RotatorConfigFragment } videoStreams { __typename ...VideoStreamInfoFragment } } fragment AdElementInfoFragment on AdElement { __typename adUnitType { __typename adType } } fragment GridInfoFragment on Grid { __typename config { __typename style } } fragment MobileLinkFragment on Link { __typename id linkLabel buttonStyle title image { __typename url } bannerImages { __typename breakPoint image { __typename url } } url renderAs linkType internalContent { __typename ...AppScreenFragment ...LinkMediaFragment ...BasicAxisContentFragment ...LinkCollection } } fragment PromoElement on PromotionalElement { __typename promotionalOneLiner summary mainImage { __typename url } mobileImage { __typename url } } fragment RotatorConfigFragment on RotatorConfig { __typename displayTotalItemCount displayTitle hideMediaTitle disableBadges } fragment VideoStreamInfoFragment on VideoStream { __typename axisId axisMediaStreamId axisCollectionId logo { __typename url } packageCode resourceCode adUnit { __typename ...BasicAdUnitFragment } name tag { __typename name id } relatedContent { __typename authConstraints { __typename authRequired } } } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } } fragment AppScreenFragment on Screen { __typename title screenCollectionType containerType id screenType } fragment LinkMediaFragment on AxisMedia { __typename id title axisId } fragment BasicAxisContentFragment on AxisContent { __typename id axisId title agvotCode axisMediaTitle description contentType duration seasonNumber episodeNumber axisMedia: axisMedia { __typename id axisId } images(formats: [POSTER, PROMO_TEASER, SQUARE, PROMO_TEASER_SMALL, THUMBNAIL]) { __typename ...ImageFragment } agvotCode axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } authConstraints { __typename ...AuthConstraintFragment } originalSpokenLanguage resourceCodes videoPlayerDestCode adUnit { __typename ...BasicAdUnitFragment } flag { __typename title label } } fragment LinkCollection on AxisCollection { __typename id axisId title collectionType gridConfig { __typename style } images(formats: [THUMBNAIL_WIDE]) { __typename url } } fragment ImageFragment on AxisImage { __typename format url } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName }"
}



COLLECTION_PAYLOAD = {
  "operationName": "posterRotator",
  "variables": {
    "subscriptions": [], # TO FILL
    "maturity": "ADULT",
    "language": "FRENCH", # TO FILL
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH", # TO FILL
    "id": "" # TO FILL
  },
  "query": "query posterRotator($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { rotator(id: $id) { __typename id title collection { __typename page { __typename totalItemCount items { __typename ...BasicMediaPosterFragment } } } config { __typename ...RotatorConfigFragment } } } fragment RotatorConfigFragment on RotatorConfig { __typename displayTotalItemCount displayTitle hideMediaTitle disableBadges } fragment BasicMediaPosterFragment on AxisMedia { __typename id title axisId agvotCode flag { __typename title label } images(formats: [POSTER]) { __typename url } resourceCodes }"
}



GRID_PAYLOAD = {
  "operationName": "grid",
  "variables": {
    "subscriptions": [],
    "maturity": "ADULT",
    "language": "FRENCH",
    "authenticationState": "AUTH",
    "playbackLanguage": "FRENCH",
    "id": "",
    "page": 0,
    "filterSelection": [
      {
        "filter": "LANGUAGE",
        "selectedIds": []
      }
    ],
    "imageFormat": [
      "POSTER"
    ]
  },
  "query": "query grid($subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!, $id: ID!, $page: Int!, $filterSelection: [FilterSelectionInput], $imageFormat: [ImageFormat]!) @uaContext(maturity: $maturity language: $language subscriptions: $subscriptions authenticationState: $authenticationState playbackLanguage: $playbackLanguage ) { grid(id: $id) { __typename id title config { __typename ...GridConfigData } collection(mode: GRID) { __typename page(page: $page, filterSelection: $filterSelection) { __typename ... CollectionPageFragment } } } } fragment GridConfigData on GridConfig { __typename style filterEnabled mediaFilters hideMediaTitle } fragment CollectionPageFragment on CollectionPage { __typename totalItemCount hasNextPage hasPreviousPage totalPageCount totalPageItemCount items { __typename id ...AxisMediaBasicInfo ...AxisCollectionDetails ...BasicAxisContentFragment } } fragment AxisMediaBasicInfo on AxisMedia { __typename id axisId title agvotCode qfrCode summary description mediaType originalSpokenLanguage mediaConstraint { __typename hasConstraintsNow } genres { __typename name } axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } images(formats: $imageFormat) { __typename ...ImageFragment } flag { __typename title label } firstAirYear ratingCodes resourceCodes heroBrandLogoId originatingNetworkLogoId } fragment AxisCollectionDetails on AxisCollection { __typename id axisId title axisCollectionItemCount gridConfig { __typename style } images(formats: [THUMBNAIL, THUMBNAIL_WIDE, POSTER]) { __typename ...ImageFragment } } fragment BasicAxisContentFragment on AxisContent { __typename id axisId title agvotCode axisMediaTitle description contentType duration seasonNumber episodeNumber axisMedia: axisMedia { __typename id axisId } images(formats: [POSTER, PROMO_TEASER, SQUARE, PROMO_TEASER_SMALL, THUMBNAIL]) { __typename ...ImageFragment } agvotCode axisPlaybackLanguages { __typename ...PlaybackLanguagesFragment } authConstraints { __typename ...AuthConstraintFragment } originalSpokenLanguage resourceCodes videoPlayerDestCode adUnit { __typename ...BasicAdUnitFragment } flag { __typename title label } } fragment PlaybackLanguagesFragment on AxisPlayback { __typename language destinationCode } fragment ImageFragment on AxisImage { __typename format url } fragment AuthConstraintFragment on AuthConstraint { __typename authRequired language packageName } fragment BasicAdUnitFragment on AxisAdUnit { __typename adultAudience heroBrand pageType product title revShare keyValue { __typename mediaType adTarget contentType pageTitle revShare subType } }"
}



