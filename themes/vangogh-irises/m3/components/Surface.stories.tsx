import type { Meta, StoryObj } from '@storybook/react';
import Surface from './Surface';

const meta  : Meta<typeof Surface> = {
  title: 'Components/Surface',
  component: Surface,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Surface>;

export const Default: Story = { args={{}} };
