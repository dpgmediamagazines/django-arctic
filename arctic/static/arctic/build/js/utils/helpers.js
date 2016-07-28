function slugify( Text ) {
    return Text
        .toLowerCase()
        .replace( /[^\w ]+/g, '' )
        .replace( / +/g, '-' );
}