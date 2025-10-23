/**
 * Core domain models representing BizDocumentAI structures.
 * These interfaces mirror the JSON captured in `tests/fixtures/*.output.json`.
 */

/**
 * Union of every non-primitive node that can appear within a block body.
 */
export type StructuredContent = Block | DictionaryBlock | ListBlock;

/**
 * Content entries within a block body. Strings represent literal paragraphs or text nodes.
 */
export type BlockContent = string | StructuredContent;

/**
 * Root document node as well as the structure shared by nested blocks and list items.
 */
export interface Block {
  kind: 'block';
  /** Optional numbering token associated with the block (e.g., "1.", "*", "2.1."). */
  number?: string;
  /** Optional heading text captured from a `<head>` tag or list item marker. */
  head?: string;
  /** Ordered body preserving nested blocks, dictionaries, lists, and raw text content. */
  body?: BlockContent[];
}

/**
 * Dictionary node emitted for `<dict>` constructs. Items preserve insertion order via object semantics.
 */
export interface DictionaryBlock {
  kind: 'dict';
  /**
   * Key/value mapping as represented in the canonical fixtures. Empty strings are permitted as values.
   */
  items: Record<string, string>;
}

/**
 * Ordered or unordered list container wrapping block items.
 */
export interface ListBlock {
  kind: 'list';
  /**
   * Each list item is represented as a block so it can carry numbering, headings, and nested content.
   */
  items: Block[];
}

/**
 * Discriminated union capturing every structured node form.
 */
export type BizDocumentNode = Block | DictionaryBlock | ListBlock;

/**
 * Top-level document type produced by the parser.
 */
export type BizDocument = Block;
